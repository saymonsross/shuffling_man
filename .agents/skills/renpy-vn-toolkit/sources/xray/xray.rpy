## КАК ПОЛЬЗОВАТЬСЯ
"""
    # включаем рентген
    $ xray = True

    # спрайт из слоёв
    layeredimage nike:
        # объединить слои
        at Flatten
        # тело
        always:
            name + "girl_body"
        always:
            # платье, которое можно просветить
            # на входе тег персонажа и полное название картинки слоя с одеждой
            XRay("girl_dress")
"""

init -2 python:
    # картинка с пятном
    xray_mask = "xray mask"

    # режим рентгена
    xray = False

    # для подсветки
    xray_light_alpha = .25 # 0 - чтобы отключить подсветку окуляров
    xray_light_color = "#fff"

## ДАЛЕЕ ЛУЧШЕ НИЧЕГО НЕ МЕНЯТЬ
    # автоматически объявляем спрайты
    images_auto()

    xray_mask_w, xray_mask_h = None, None

    # класс для картинок, реагирующих на xray
    class XRay(renpy.Displayable):
        def __init__(self, child, **kwargs):
            super(XRay, self).__init__(**kwargs)
            self.child = renpy.displayable(child)
            self.mouse_x, self.mouse_y = 0, 0
            self.width, self.height = 0, 0

        def render(self, width, height, st, at):
            global xray

            # если рентген включен
            if xray:
                # размер пятна
                if xray_mask_w is None:
                    store.xray_mask_w, store.xray_mask_h = get_size(xray_mask)
                # положение
                x = int(self.mouse_x - xray_mask_w / 2)
                y = int(self.mouse_y - xray_mask_h / 2)
                # маска из пятна
                t = ImageMask(self.child, Flatten(Composite((width, height), (0, 0), "#fff", (x, y), At(xray_mask, paint("#000")))))
            # если рентген выключен
            else:
                t = self.child

            child_render = renpy.render(t, width, height, st, at)
            self.width, self.height = child_render.get_size()
            render = renpy.Render(self.width, self.height)
            render.blit(child_render, (0, 0))
            return render

        def event(self, ev, x, y, st):
            self.mouse_x, self.mouse_y = x, y
            renpy.redraw(self, 0)
            return self.child.event(ev, x, y, st)

        def visit(self):
            return [ self.child ]

    # для подсветки
    def xray_at_f(trans, st, at):
        # размер пятна
        if xray_mask_w is None:
            store.xray_mask_w, store.xray_mask_h = get_size(xray_mask)
        x, y = renpy.get_mouse_pos()
        trans.pos = int(x), int(y)
        if xray:
            trans.alpha = xray_light_alpha
        else:
            trans.alpha = 0
        return 1/30.

    config.overlay_screens.append("xray")

init:
    # для подсветки
    transform xray_at:
        anchor(.5, .5)
        function xray_at_f

screen xray:
    add xray_mask at paint(xray_light_color), xray_at
