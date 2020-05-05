import time
import re
import os
import uuid
from urllib.parse import urljoin, urlparse
from hamcrest import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pytest_testconfig import config as PyConf
from util.logger import LOGGER
from util import session


class Browser:

    def __init__(self):
        self.new_driver()

    _driver_instance = None
    _session_snapshots = {}

    def new_driver(self):
        command_executor = "{0}://{1}:{2}{3}".format(
            PyConf['protocol'],
            PyConf['host'],
            PyConf['port'],
            PyConf['path']
        )

        remote_driver = webdriver.Remote(
            command_executor=command_executor,
            desired_capabilities=PyConf.get('capabilities')
        )
        self._driver_instance = remote_driver

        self._driver_instance.implicitly_wait(PyConf.get('implicit_timeout'))
        self._driver_instance.maximize_window()

        return self._driver_instance

    def get_driver(self):
        if not self._driver_instance:
            self.new_driver()
        return self._driver_instance

    def close_driver(self):
        if self._driver_instance:
            self._driver_instance.quit()
            self._driver_instance = None

    def open(self, path):
        """
        Переходит по относительному URL (/login, /admin/users, etc ...)

        Args:
            path (str): Путь

        Examples:
            >>> browser.open("/")
            # На главную

            >>> browser.open("/admin")
            # В админку
        """
        url = urljoin(PyConf.get('url'), path)
        LOGGER.info(f"Open {url}")
        self._driver_instance.get(url)

    def open_url(self, url):
        """
        Переходит по абсолютному URL.

        Args:
            url (str): URL

        Examples:
            >>> browser.open_url("https://google.com")
        """
        LOGGER.info(f"Open URL {url}")
        self._driver_instance.get(url)

    def refresh(self):
        """
        Обновляет страницу
        """
        LOGGER.info("Refresh page")
        self._driver_instance.refresh()

    def grab_console_log(self):
        '''
        Получить лог браузерной консоли. Буффер очищается после каждого запроса.
        Требует сapability ``loggingPrefs: { browser: 'INFO' }``.

        Returns:
            list[str]: список строк
        '''
        LOGGER.info("Grab browser console log")
        return self._driver_instance.get_log('browser')

    def grab_page_html(self):
        """
        Возвращает html всей страницы.

        Returns:
            str: html
        """
        LOGGER.info("Grab page html")
        return self._driver_instance.page_source

    def grab_html_from(self, element):
        """
        Возвращает html элемента.

        Returns:
            str: html
        """
        LOGGER.info(f"Grab html from {element}")
        el = self._match_first_or_fail(element)
        return el.get_attribute('outerHTML')

    def clear_field(self, input_element):
        """
        Очищает поле.

        Args:
            input_element (Element): Поле ввода

        Examples:
            >>> browser.clear_field(Element("#input"))
        """
        LOGGER.info(f"Clear field {input_element}")
        el = self._match_first_or_fail(input_element)
        el.clear()

    def fill_field(self, element, text):
        """
        Заполняет текстом поле ввода

        Args:
            element (Element): Поле ввода
            text    (str):  Текст

        Examples:
            >>> browser.fill_field(Element("//input[@type='text']"), "Hello World!")
        """
        LOGGER.info(f"Fill field {element} with '{text}'")
        el = self._match_first_or_fail(element)
        el.clear()
        el.send_keys(text)

    def fill_field_with_delay(self, element, text, delay=0.1):
        """
        Заполняет текстом поле ввода делая паузу между каждым символом.

        Args:
            element (Element): Поле ввода
            text    (str):  Текст
            delay   (float, optional): Задержка (сек.), по умолчанию 0.1

        Examples:
            >>> browser.fill_field(Element("//input[@type='text']"), "Hello World!", 0.2)
        """
        LOGGER.info(f"Fill field {element} with '{text}' & delay '{delay}'")
        field = self._match_first_or_fail(element)
        for ch in text:
            field.send_keys(ch)
            self.sleep(delay)

    def press_key(self, element, *chars):
        """
        Нажимает кнопки.
        Чтобы ввести символы с модификатором (ctrl, alt, shift, meta), передай кортеж
        у которого первый элемент модификатор, а второй текст.

        Args:
            element (Element):      Элемент, куда посылать нажатия
            *chars  (str|tuple):    Что вводить. Может быть строкой или кортежем в модификатором

        Examples:
            Дано: поле, в которое введён текст ``old``:\n
            ``<input id="input" value="old" />``

            >>> from selenium.webdriver.common.keys import Keys
            >>> field = Find("#input")
            >>> browser.press_key(field, "A")
            oldA
            >>> browser.press_key(field, ("ctrl", "a"), "new")
            new
            >>> browser.press_key(field, ("shift", "333"), "2", "x")
            old###2x
            >>> browser.press_key(field, Keys.BACKSPACE)
            ol
        """
        LOGGER.info(f"Press keys {chars} on {element}")
        el = self._match_first_or_fail(element)
        for char in chars:
            el.send_keys(*self._convert_key_modifier(char))

    def append_field(self, element, text):
        """
        Присоединяет переданный текст к элементу.

        Args:
            element     (Element): элемент
            text        (str): текст

        Examples:
            >>> browser.append_field(Find('#field'), 'foo bar baz')
        """
        LOGGER.info(f"Append field {element}, '{text}'")
        field = self._match_first_or_fail(element)
        field.send_keys(text)

    def wait_for_element_visible(self, element, timeout=5):
        """
        Ждёт до ``timeout`` сек. видимости элемента.
        Если элемент не появился, бросает timeout exception.

        Args:
            element (Element): Элемент, который ждём
            timeout (int, optional): Таймаут ожидания (сек.), по умолчанию 5.

        Raises:
            TimeoutException

        Examples:
            >>> browser.wait_for_element_visible(Element("#header", 15))

        """
        LOGGER.info(f"Wait for element visible {element}")
        condition = EC.visibility_of_element_located(element.locator())
        self.wd_wait(timeout).until(condition)

    def wait_for_element_not_visible(self, element, timeout=5):
        """
        Ждёт до ``timeout`` сек. исчезновения элемента.
        Если элемент остался видимым, бросает timeout exception.

        Args:
            element (Element): Элемент, который ждём
            timeout (int, optional): Таймаут ожидания (сек.), по умолчанию 5.

        Raises:
            TimeoutException

        Examples:
            >>> browser.wait_for_element_not_visible(Element("#header", 15))
        """
        LOGGER.info(f"Wait for element not visible {element}")
        condition = EC.invisibility_of_element_located(element.locator())
        self.wd_wait(timeout).until(condition)

    def see_element(self, element, attributes={}):
        """
        Проверяет, что элемент существует и видим.
        Также можно указать атрибуты этого элемента.

        Args:
            element (Element): Элемент
            attributes (dict, optional): Словарь атрибутов

        Examples:
            >>> browser.see_element(Element("tr"))
            >>> browser.see_element(Element("tr"), {"some-attr": "some-value"})
        """
        LOGGER.info(f"See element {element}, {attributes}")
        self._enable_implicit_wait()
        els = self._match_visible(element)
        self._disable_implicit_wait()
        els = self._filter_by_attributes(els, attributes)
        assert_that(els, is_not(empty()))

    def see_text(self, text, element=None):
        """
        Проверяет, что страница содержит текст (с учётом регистра).
        Можно передать элемент, чтобы искать текст только в нём.

        Args:
            text (str): Искомый текст
            element (Element, optional): Элемент

        Examples:
            >>> browser.see_text("Администрирование")
            >>> browser.see_text("Выйти", Element("h1"))
        """
        LOGGER.info(f"See text {text} in {element}")
        self._enable_implicit_wait()
        text_from_page = self.grab_visible_text(element)
        self._disable_implicit_wait()
        assert_that(text_from_page, contains_string(text))

    def see_in_field(self, input_element, needle):
        """
        Проверяет, что текст поля ввода равен переданному значению.

        Args:
            input_element (Element): Элемент
            needle (str): Текст

        Examples:
            >>> browser.see_in_field(Element("input#foo"), "Hello World!")
        """
        LOGGER.info(f"See text '{needle}' in field {input_element}")
        val = self.grab_value_from(input_element)
        assert_that(val, equal_to(needle))

    def see_number_of_elements(self, element, expected):
        """
        Проверяет, что на странице определённое кол-во элементов.

        Args:
            element (Element): Элемент
            expected (int|tuple): Ожидаемое кол-во

        Returns:
            None

        Raises:
            AssertionError

        Examples:
            >>> browser.see_number_of_elements( E('tr'), 10 )
            >>> browser.see_number_of_elements( E('tr'), (4, 6) ) # Между 4 и 6, включительно
        """
        LOGGER.info(f"See number of elements {element}, {expected}")
        count = len(self._match_visible(element))
        if isinstance(expected, tuple):
            a, b = expected
            assert_that(a <= count <= b, is_(True),
                        f'Number of elements expected to be in range {expected}, but was {count}')
        else:
            assert_that(count, equal_to(expected),
                        f'Number of elements expected to be {expected}, but was {count}')

    def grab_visible_text(self, element=None):
        """
        Получает видимый текст всей страницы или элемента.

        Args:
            element (Element, optional): Элемент

        Returns:
            str: Текст

        Examples:
            >>> browser.grab_visible_text()
            >>> browser.grab_visible_text(Element("h1"))
        """
        LOGGER.info(f"Get visible text from {element}")
        if element is not None:
            return self.grab_text_from(element)

        els = self._match(self._driver_instance.find_element_by_css_selector("body"))
        if len(els) == 0:
            return ''

        return els[0].text

    def click(self, element):
        """
        Кликает по элементу.

        Args:
            element (Element): Элемент

        Examples:
            >>> browser.click(Element("#logout"))
        """
        LOGGER.info(f"Click {element}")
        self._match_first_or_fail(element).click()

    def grab_visible(self, element):
        """
        Получает видимые элементы.

        Args:
            element (Element, optional): Элемент

        Returns:
            selenium.webdriver.remote.webelement.WebElement[]: Список элементов

        Examples:
            >>> browser.grab_visible(Element("th"))
        """
        LOGGER.info(f"Grab visible {element}")
        return self._match_visible(element)

    def grab_text_from(self, element):
        """
        Получает текст элемента.

        Args:
            element (Element): Элемент

        Returns:
            str: Текст

        Examples:
            >>> browser.grab_text_from(Element("h1"))
        """
        LOGGER.info(f"Grab text from {element}")
        el = self._match_first_or_fail(element)
        return el.text

    def grab_attribute_from(self, element, attribute):
        """
        Получает значение атрибута.

        Args:
            element     (Element): Элемент
            attribute   (str):  Атрибут

        Returns:
            str: Значение атрибута

        Examples:
            ``<span id="tooltip" title="hello_world"> </span>``

            >>> browser.grab_attribute_from(Element('#tooltip'), 'title')
            "hello_world"
        """
        LOGGER.info(f"Grab attribute from {element}")
        el = self._match_first_or_fail(element)
        return el.get_attribute(attribute)

    def grab_value_from(self, input_element):
        """
        Получает value атрибут из поля.
        Используется, чтобы получить введённый текст.

        Args:
            element (Element): Элемент

        Returns:
            str: Значение value атрибута

        Examples:
            ``<input id="login" value="ivanov">``

            >>> browser.grab_value_from(Element('#login'))
            "ivanov"
        """
        LOGGER.info(f"Grab value from {input_element}")
        el = self._match_first_or_fail(input_element)
        return el.get_attribute('value')

    def grab_multiple(self, elements):
        """
        Получает тексты подходящих элементов и возващает их как список.

        Args:
            element (Element): Элемент

        Returns:
            str[]: Список текстов

        Examples:
            .. code-block:: html

                <tr> foo </tr>
                <tr> bar </tr>
                <tr> baz </tr>


            >>> browser.grab_multiple( Element('tr') )
            ["foo", "bar", "qaz"]
        """
        LOGGER.info(f"Grab multiple {elements}")
        els = self._match(elements)
        return list(map(lambda el: el.text, els))

    def save_screenshot(self, name=None):
        """
        Делает скриншот видимой части страницы и сохраняет в ``_output/debug``.

        Args:
            name (str, optional): Имя файла

        Returns:
            pathlib.Path: Путь до файла
        """
        debug_dir = session.output_dir.joinpath('debug')
        if not os.path.exists(debug_dir):
            os.mkdir(debug_dir)

        if name is None:
            name = uuid.uuid4()

        file_path = debug_dir.joinpath(f"{name}.png")
        LOGGER.info(f"Save screenshot to {file_path}")
        self._driver_instance.get_screenshot_as_file(str(file_path))
        return file_path

    def get_screenshot_binary(self):
        """
        Возвращает скриншот в бинарном формате.

        Returns:
            bytes
        """
        LOGGER.info(f"Get screenshot as png")
        return self._driver_instance.get_screenshot_as_png()

    def move_mouse_over(self, element):
        """
        Передвигает курсор в центр элемента

        Args:
            element (Element): элемент
        """
        LOGGER.info(f"Move mouse over {element}")
        el = self._match_first_or_fail(element)
        ActionChains(self._driver_instance).move_to_element(el).perform()

    def switch_to_iframe(self, frame=None):
        """
        Переключяет контекст в iframe.
        Чтобы перейти в родительский фрейм - вызывается без параметров.

        Args:
            frame (Element): iframe

        Examples:
            ``<iframe name="another_frame" src="http://example.com">``

            >>> frame = Element("frame[name = 'another_frame']")
            >>> browser.switch_to_iframe(frame)
            >>> browser.switch_to_iframe() # в родительский фрейм
        """
        LOGGER.info(f"Switch to iframe {frame}")
        if frame is not None:
            el = self._match_first_or_fail(frame)
            self._driver_instance.switch_to.frame(el)
        else:
            self._driver_instance.switch_to.parent_frame()

    def save_session_snapshot(self, name):
        """
        Сохраняет куки чтобы загрузить их в другом тесте.
        Например, если в каждом тесте необходима авторизация,
        можно выполнить этот сценарий единожды,
        а в других тестах только восстанавливать сессию.

        Args:
            name (str): Название сесиии

        Examples:
            >>> def login():
            >>>     # Если сессия существует - пропустить логин
            >>>     if browser.load_session_snapshot("login"):
            >>>         return
            >>>     browser.fill_field( Element("#username") )
            >>>     browser.fill_field( Element("#password") )
            >>>     browser.click( Element("#submit") )
            >>>     browser.save_session_snapshot("login")
        """
        LOGGER.info(f"Save session snapshot '{name}'")
        self._session_snapshots[name] = self._driver_instance.get_cookies()

    def load_session_snapshot(self, name):
        """
        Загружает сохранённую сессию.
        Смотри :func:`~wd.browser.Browser.save_session_snapshot`.

        Args:
            name (str): Имя сессии

        Returns:
            bool
        """
        LOGGER.info(f"Load session snapshot '{name}'")
        if name not in self._session_snapshots:
            return False

        for cookie in self._session_snapshots[name]:
            self.set_cookie(cookie["name"], cookie["value"], cookie)

        return True

    def set_cookie(self, name, value, params={}):
        """
        Задаёт куку с именем и значением.
        Можно передать дополнительные параметры.

        Args:
            name    (str): Имя куки
            value   (str): Значение куки
            params  (dict, optional):
                Доп. параметры:

                    - domain
                    - path
                    - expiry
                    - secure
                    - httpOnly
        """
        LOGGER.info(f"Set cookie '{name}': '{value}'")
        params["name"] = name
        params["value"] = value

        if "domain" not in params:
            url_parts = urlparse(PyConf.get("url"))
            if "netloc" in url_parts:
                params["domain"] = url_parts["netloc"]

        defaults = {
            "path": '/',
            "expiry": int(time.time()) + 86400,
            "secure": False,
            "httpOnly": False,
        }

        for k, v in defaults.items():
            if k not in params:
                params[k] = v

        self._driver_instance.add_cookie(params)

    def scroll_to(self, element, offset_x=0, offset_y=0):
        """
        Скроллит к центру переданного элемента.
        Дополнительное смещение, расчитываемое от левого верхнего угла элемента,
        можно задать параметрами `offset_x` и `offset_y` (в пикселях).

        Важно: вызывает метод scrollTo на объекте window.
        Если элемент находится в каком то контейнере с `overflow: scoll`,
        то данный метод не сработает, см. :func:`~wd.browser.Browser.scroll_into_view`.

        Args:
            element     (Element): элемент
            offset_x    (int, optional): смещение по X (px)
            offset_y    (int, optional): смещение по Y (px)
        """
        LOGGER.info(f"Scroll to {element}")
        el = self._match_first_or_fail(element)
        x = el.location['x'] + offset_x
        y = el.location['y'] + offset_y
        self.execute_js(f"window.scrollTo({x}, {y})")

    def scroll_into_view(self, element, offset_x=0, offset_y=0):
        LOGGER.info("Scroll into view")
        el = self._match_first_or_fail(element)
        self.execute_js(f"arguments[0].scrollIntoView({offset_x}, {offset_y})", el)

    def delete_all_cookies(self):
        """
        Удаляет все куки.
        """
        LOGGER.info("Delete all cookies")
        self._driver_instance.delete_all_cookies()

    def element_has_attribute(self, element, attr, expected_value=None):
        """
        Проверяет наличие атрибута у элемента.
        Опционально приинимает значение атрибута.

        Args:
            element         (Element): Элемент
            attr            (str): Имя атрибута
            expected_value  (string, optional): Ожидаемое значание

        Returns:
            bool

        Examples:
            ``<div class='foo bar bazqux'> </div>``

            >>> browser.element_has_attribute( Element('div'), 'class' )
            True
            >>> browser.element_has_attribute( Element('div'), 'class', 'foo' )
            True
            >>> browser.element_has_attribute( Element('div'), 'class', 'baz' )
            False
        """
        LOGGER.info(f"Element {element} has attribute {attr}: {expected_value}")
        actual_val = self.grab_attribute_from(element, attr)

        if actual_val is None:
            return False
        elif expected_value is None:
            return True
        else:
            values_list = re.sub(r'\s+', ' ', actual_val).strip().split(' ')
            if expected_value in values_list:
                return True
            else:
                return False

    def execute_js(self, script, *args):
        """
        Выполняет js на странице.

        Args:
            script  (str): JS скрипт
            *args   (obj): Аргументы

        Returns:
            То, что возвращает скрипт.

        Examples:
            ``<span id="tooltip" data-attr="foo"> </span>``

            >>> script = 'return arguments[0].getAttribute("data-attr");'
            >>> browser.execute_js(script, browser.find(Element("#tooltip")))
            "foo"
        """
        LOGGER.info(f"Execute JS '{script}'")
        return self._driver_instance.execute_script(script, *args)

    def sleep(self, secs):
        """
        Просто ждёт ``secs`` секунд.

        Args:
            secs (float): Сколько секунд спать

        Raises:
            Exception: Если передали больше 1000 сек.
        """
        LOGGER.info(f"Sleep {secs}")
        if secs >= 1000:
            raise Exception("Waiting for more then 1000 seconds: 16.6667 mins")
        time.sleep(secs)

    def wd_wait(self, timeout=10, poll_frequency=0.5):
        """
        Возвращает объект WebDriverWait.

        Args:
            timeout         (int, optional): Таймаут ожидания, по умолчанию 10
            poll_frequency  (float, optional): Частота опроса, по умолчанию 0.5

        Returns:
            WebDriverWait
        """
        return WebDriverWait(self._driver_instance, timeout, poll_frequency)

    def scroll_top(self):
        LOGGER.info("Window scroll top")
        self.execute_js("window.scrollTo(0, 0)")

    def find(self, element):
        context = self._driver_instance
        try:
            if element.ctx is not None:
                context = self.find(element.ctx)

            return context.find_element(*element.locator())
        except NoSuchElementException as e:
            e.msg = f"No such element: Unable to locate element: {element}"
            raise

    def finds(self, element):
        context = self._driver_instance
        if element.ctx is not None:
            context = self.find(element.ctx)

        return context.find_elements(*element.locator())

    def _filter_by_attributes(self, els, attributes):
        for k, v in attributes.items():
            els = list(filter(
                lambda el: el.get_attribute(k) == v,
                els))
        return els

    def _match_visible(self, element):
        els = self._match(element)
        nodes = list(filter(
            lambda el: el.is_displayed(),
            els))
        return nodes

    def _match_first_or_fail(self, element):
        self._enable_implicit_wait()
        els = self._match(element)
        self._disable_implicit_wait()
        if not els:
            raise Exception("Element {0} was not found.".format(element))
        return els[0]

    def _match(self, element):
        return self.finds(element)

    def _enable_implicit_wait(self):
        self._driver_instance.implicitly_wait(PyConf['implicit_timeout'])

    def _disable_implicit_wait(self):
        self._driver_instance.implicitly_wait(0)

    def _convert_key_modifier(self, keys):
        if not isinstance(keys, tuple):
            return (keys,)
        if keys[0] in ["ctrl", "contol"]:
            return (Keys.CONTROL, keys[1])
        if keys[0] == "alt":
            return (Keys.ALT, keys[1])
        if keys[0] == "shift":
            return (Keys.SHIFT, keys[1])
        if keys[0] == "meta":
            return (Keys.META, keys[1])
        return keys