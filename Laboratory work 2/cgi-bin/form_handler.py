import cgi

form = cgi.FieldStorage()

username = form.getvalue("username")
language = form.getvalue("language")
language_radio = form.getvalue("language_radio")
language_check = form.getlist("language_check")


print("Content-type: text/html\n")
print("""
    <title>Result</title>
    <meta charset="UTF-8">
    <link rel="stylesheet" type="text/css" href="../styles/style.css">
    <center>
""")
if not username or not language or not language_check:
    print("<h2 class='error'>Заповність всі поля,будь ласка!</h2></center>")
else:
    print(f"""
    <h2>Результат</h2>
    <p>Твоє ім'я : <span>{username}</span></p>
    <p>Твоя улюблена мова програмування : <span>{language}</span></p>
    <p>Між С++ та Python для парсингу ти обереш : <span>{language_radio}   
    <p>Мови(-а) програмування , з якими ти працював : <span> {language_check}""")
print("""

</center>
""")