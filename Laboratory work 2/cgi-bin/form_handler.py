import cgi
import os
import http.cookies

def getCookieValue(key):
    if "HTTP_COOKIE" in os.environ:
        cookie_string = os.environ.get("HTTP_COOKIE")
        cookies = http.cookies.SimpleCookie()
        cookies.load(cookie_string)
        if key in cookies:
            return cookies[key].value
    return None

def delete_cookie(cookie_name):
    expired_date = 'expires=Wed, 28 Aug 2013 18:30:00 GMT'
    print("Set-Cookie: %s=This could be anything. The important part is the key name xml_edit_tool; %s \r\n" % (cookie_name, expired_date))

form = cgi.FieldStorage()

username = form.getvalue("username")
language = form.getvalue("language")
language_radio = form.getvalue("language_radio")
language_check = form.getlist("language_check")

headerString = (f"""Content-type: text/html\n
    <title>Result</title>
    <meta charset="UTF-8">
    <link rel="stylesheet" type="text/css" href="../styles/style.css">
    <center>
""")

if not username or not language or not language_check:
    print(headerString)
    print("<h2 class='error'>Заповність всі поля,будь ласка!</h2>")
    print("<button class='buttonclass'><a style='text-decoration:none;color:white' href='http://localhost:9999/'>Повернутися до попередньої сторінки</a></button></center>")

else:

    print(f"Set-cookie: username={username};")
    print(f"Set-cookie: language={language};")
    print(f"Set-cookie: languageradio={language_radio};")

    name_cookie = getCookieValue("username")
    language_cookie = getCookieValue("language")
    languageradio_cookie = getCookieValue("languageradio")


    print(headerString)
    print(f"""
    <h2>Результат</h2>
    <p>Твоє ім'я : <span>{username}</span></p>
    <p>Твоя улюблена мова програмування : <span>{language}</span></p>
    <p>Між С++ та Python для парсингу ти обереш : <span>{language_radio}   
    <p>Мови(-а) програмування , з якими ти працював : <span> {language_check}</p>
    <p>Інформація з cookies : <span>username = {name_cookie},language = {language_cookie},languageradio = {languageradio_cookie}
    <form action="delete_cookies.py">
    <input class="buttonclass" type="submit" value="Видалити всі cookies">
    </form>
    """)


print("""
</center>
""")