from mako.template import Template

mytemplate = Template("")
print(mytemplate.render())

# Choose genre:  |  Выберите жанр:  |  

en = { 
  'choose_genre': Template("Choose genre:"),
  'undefined_lang': Template("Language was not defined. Supported languages: ru, en. E.g: /lang ru"),
  'confirmed_lang':Template("Language was succesfully updated."),
  'anime_inf': Template("""\
<%!
    import helper
%>
*Title: ${anime.name | helper.escape}*
*Genres:* 
% for genre in anime.genres: 
${genre["name"]} \\
% endfor
  """)
}

ru = {
  'choose_genre': Template("Выберите жанр:"),
  'undefined_lang': Template("Язык не определен. Поддерживаемые языки: ru, en. Например: /lang ru"),
  'confirmed_lang':Template("Язык был успешно обновлен."),
  'anime_inf': Template("""\
<%!
    import helper
%>
*Название: ${anime.russian | helper.escape}*
*Описание:* ${anime.description | helper.escape}
*Жанры:* 
% for genre in anime.genres: 
${genre["russian"]} \\
% endfor
  """)
}

[]
# t("anime_inf", "ru", anime=anime)

def t(message,language, **kwargs):
  # Выбрать либо en либо ru
  # Найти ключ message
  # Зарендерить и вернуть
  locale = en
  if language == "ru":
    locale = ru
  template = locale[message]
  
  return template.render(**kwargs)
