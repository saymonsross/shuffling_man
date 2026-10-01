## Персонажи — единственное место определения. Реестр — docs/01_characters.md.
## Имена только через _("…"); вариации имени — Character с kind=<база>;
## в логике/сейвах сравнивать ключи, не отображаемые строки.
## Цвет имени общий для всех — стиль say_label (screens.rpy).

## Марина Александровна Шрайбер — главная героиня, рассказчица.
define mar = Character(_("Марина"))

## Витя — муж Марины. talk_callback: на его репликах двигается рот у кадров, которые
## слушают ключ "vit" (common/transforms.rpy).
define vit = Character(_("Витя"), callback=talk_callback("vit"))
define vit_d = Character(_("Витенька"), kind=vit)

## Настя — дочь Марины и Вити.
define nas = Character(_("Настя"))
define nas_d = Character(_("Настенька"), kind=nas)

define pol = Character(_("Полли"))

define sos = Character(_("Соседка"))

define psi = Character(_("Психолог"))
