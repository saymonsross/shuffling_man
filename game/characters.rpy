## Персонажи — единственное место определения. Реестр — docs/01_characters.md.
## Имена только через _("…"); вариации имени — Character с kind=<база>;
## в логике/сейвах сравнивать ключи, не отображаемые строки.
## Цвет имени общий для всех — стиль say_label (screens.rpy).

## Реплика вслух начинается с тире — в отличие от мыслей рассказчицы. Тире ставит движок
## всем, кто наследует speech: в текст реплик его не писать.
define speech = Character(None, what_prefix="— ")

## talk_callback: на репликах персонажа двигается рот у кадров, которые слушают его ключ
## (common/transforms.rpy).

## Марина Александровна Шрайбер — главная героиня, рассказчица.
define mar = Character(_("Марина"), kind=speech, callback=talk_callback("mar"))

## Витя — муж Марины.
define vit = Character(_("Витя"), kind=speech, callback=talk_callback("vit"))
define vit_d = Character(_("Витенька"), kind=vit)

## Настя — дочь Марины и Вити.
define nas = Character(_("Настя"), kind=speech, callback=talk_callback("nas"))
define nas_d = Character(_("Настенька"), kind=nas)

define pol = Character(_("Полли"), kind=speech)

define sos = Character(_("Соседка"), kind=speech, callback=talk_callback("sos"))

define psi = Character(_("Психолог"), kind=speech)

## Голос из телевизора — реплика баблом у экрана (экран c1s1_bark_say, глава 1, сцена 1).
## what_style: стиль say_dialogue сдвинул бы текст из рамки бабла.
define tvv = Character(_("ТЕЛЕВИЗОР"), screen="c1s1_bark_say", what_style="c1s1_vitya_bark_text",
    show_side="right", show_pos=(1152, 180), show_width=760)
