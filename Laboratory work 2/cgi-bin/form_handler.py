import cgi
import os

def get_cookie(_match):
  if 'HTTP_COOKIE' in os.environ:
    cookies = os.environ['HTTP_COOKIE']
    cookies = cookies.split('; ')
    for cookie in cookies:
        try:
            (_name, _value) = cookie.split('=')
            if (_match.lower() == _name.lower()):
                return _value
        except:
            return ('')
  return('')

def val(_string):
  try:
    return int(_string)
  except:
    return 0


form = cgi.FieldStorage()

username = form.getvalue("username")
language = form.getvalue("language")
language_radio = form.getvalue("language_radio")
language_check = form.getlist("language_check")

headerString = (f"""Content-type: text/html\n
    <title>Result</title>
    <meta charset="UTF-16">
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
    print('Set-Cookie: Count=' + str(val(get_cookie('Count')) + 1))

    name_cookie = get_cookie('username')
    language_cookie = get_cookie('language')
    languageradio_cookie = get_cookie('languageradio')


    print(headerString)
    print(f"""
    <h2>Результат</h2>
    <p>Твоє ім'я : <span>{username}</span></p>
    <p>Твоя улюблена мова програмування : <span>{language}</span></p>
    <p>Між С++ та Python для парсингу ти обереш : <span>{language_radio}   
    <p>Мови(-а) програмування , з якими ти працював : <span> {language_check}</p>
    <p>Інформація з cookies : <span>Кількість cookie = {str(val(get_cookie('Count')))},username = {name_cookie},language = {language_cookie},languageradio = {get_cookie('languageradio')}
    <form action="delete_cookies.py">
    <input class="buttonclass" type="submit" value="Видалити всі cookies">
    </form>
    <button class='buttonclass'><a style='text-decoration:none;color:white' href='http://localhost:9999/'>Повернутися до попередньої сторінки</a></button>

    """)


print("""
</center>
""")