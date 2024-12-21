"""
Python kivy программа для расчета стоимости услуг по водоснабжению.

"""

import os
import pandas as pd
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogButtonContainer, MDDialogSupportingText

from kivy.lang import Builder

os.environ['KIVY_IMAGE'] = 'pil'

KV = """

MainScreen:
    id: main
    
    MDNavigationLayout:
    
        MDScreenManager:
        
            MDScreen:
                
                FitImage:
                    id: bck_image
                    size_hint_x: 1
                    size_hint_y: 1
                    source: 'bkg.jpeg'
                    color: [.2, .27, .46, 0.2]
                    
                MDBoxLayout:
                    id: box1
                    orientation: 'vertical'
                    
                    MDTopAppBar:
                        id: top
                        type: 'small'
                        size_hint_x: 1
                        size_hint_y: .1
                        pos_hint: {'center_x': .5, 'center_y': .5}
                        
                        MDTopAppBarLeadingButtonContainer:
                            MDActionTopAppBarButton:
                                icon: 'cog-outline'
                                pos_hint: {'center_x': .5, 'center_y': .5}
                                on_release: nav_drawer.set_state('toggle')
                                
                                
                        MDTopAppBarTitle:
                            text: 'Расчет счетчиков'
                            font_style: 'Headline'
                            color: '50638F'
                            halign: 'right'
                            bold: True
                            role: 'medium'
                            pos_hint: {'center_x': .5, 'center_y': .5}
                            
                        #MDTopAppBarTrailingButtonContainer:
                            #size_hint_x: .1
                            
                    MDBoxLayout:
                        id: box2
                        size_hint_y: .9
                        orientation: 'vertical'
                        padding: 10
                        spacing: 15
                        
                        MDTextField:
                            id: cold_label
                            md_bg_color: 0, 0, 0, .5
                            mode: 'outlined'
                            size_hint_x: 1
                            radius: 24
                            
                            MDTextFieldLeadingIcon:
                                # icon: 'coldwatericon.png'
                                icon: 'snowflake'
                                theme_icon_color: 'Custom'
                                icon_color_normal: '697DAB'
                            
                            MDTextFieldHintText:
                                text: 'Объем ХВ, куб. м'
                            
                        MDTextField:
                            id: hot_label
                            mode: 'outlined'
                            size_hint_x: 1
                            radius: 24
                            
                            MDTextFieldLeadingIcon:
                                # icon: 'coldwatericon.png'
                                icon: 'fire'
                                theme_icon_color: 'Custom'
                                icon_color_normal: 'D2778E'
                                        
                            MDTextFieldHintText:
                                text: 'Объем ГВ, куб. м'
            
                        MDBoxLayout:
                            orientation: 'horizontal'
                            size_hint_y: .25
                            
                            MDLabel:
                                id: w_result
                                font_style: 'Headline'
                                role: 'medium'
                                color: '50638F'
                                text: 'ИТОГО: '
                                    
                            MDLabel:
                                id: w_result_label
                                text: str()
                                halign: 'center'
                                font_style: 'Headline'
                                role: 'medium'
                                color: '415589'
                                bold: True
                                
                        MDLabel:
                            id: label_out
                            size_hint: 1, .5
                            md_bg_color: app.theme_cls.backgroundColor
                            pos_hint: {'center_x': .5, 'center_y': .5}
                            font_style: 'Title'
                            role: 'medium'
                            halign: 'left'
                            valign: 'top'
                            adaptive_width: False
                            padding: '5dp', '5dp'
                            theme_text_color: 'Custom'
                            text_color: '7182AB'
                            allow_copy: True 
                            markup: True
                            text: ''
                    
                        MDButton:
                            id: calc
                            size_hint: .4, None
                            height: root.height/12
                            pos_hint: {'center_x': .5, 'center_y': .5}
                            on_release: root.calculation()
                            style: 'filled'
                    
                            MDButtonText:
                                text: 'Рассчитать'
                                font_style: 'Title'
                                bold: True
        MDNavigationDrawer:
            id: nav_drawer
            radius: 0, dp(24), dp(24), 0
            
            MDNavigationDrawerMenu:
                spacing: 20
                padding: 20
                adaptive_size: True
                
                MDNavigationDrawerLabel:
                    text: 'Настройки'
                    font_style: 'Headline'
                    role: 'small'
                    color: '50638F'
                    bold: True
                    halign: 'center'
                    valign: 'bottom'
                    pos_hint: {'center_x': 1, 'center_y': 1}
                
                MDWidget:
                    size_hint_x: 1
                    size_hint_y: None
                        
                MDDivider:
                    size_hint_x: 1
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    
                MDWidget:
                    size_hint_x: 1
                    size_hint_y: None
                    
                MDBoxLayout:
                    spacing:15
                    size_hint_y: .25
                    
                    MDLabel:
                        markup: True
                        text: 'Тариф ХВ, руб/м[sup]3[/sup]'
                        valign: 'bottom'
                        pos_hint: {'center_x': .5, 'center_y': .5}
                        
                    MDTextField:
                        id: cwaterprice
                        mode: 'filled'
                        pos_hint: {'center_x': .5, 'center_y': .5}
                        text: str(root.cwaterprice)
                        valign: 'center'
                            
                        MDTextFieldHintText:
                            text: 'текущий'
                
                MDWidget:
                    size_hint_x: 1
                    size_hint_y: None
                
                MDDivider:
                    size_hint_x: 1
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    
                MDWidget:
                    size_hint_x: 1
                    size_hint_y: None
                
                MDBoxLayout:
                    spacing:15
                    size_hint_y: .25
                    
                    MDLabel:
                        markup: True
                        text: 'Тариф тепл. эн., руб/Гкал'
                        valign: 'bottom'
                        pos_hint: {'center_x': .5, 'center_y': .5}
                        
                    MDTextField:
                        id: gcalprice
                        mode: 'filled'
                        pos_hint: {'center_x': .5, 'center_y': .5}
                        text: str(root.gcalprice)
                        valign: 'center'
                            
                        MDTextFieldHintText:
                            text: 'текущий'
                
                MDWidget:
                    size_hint_x: 1
                    size_hint_y: None
                    
                MDDivider:
                    size_hint_x: 1
                    pos_hint: {'center_x': .5, 'center_y': .5}
                
                MDWidget:
                    size_hint_x: 1
                    size_hint_y: None
                        
                MDBoxLayout:
                    spacing:15
                    size_hint_y: .25
                    MDLabel:
                        markup: True
                        text: 'Тариф водоотв., руб/м[sup]3[/sup]'
                        valign: 'bottom'
                        pos_hint: {'center_x': .5, 'center_y': .5}
                        
                    MDTextField:
                        id: waterback
                        mode: 'filled'
                        pos_hint: {'center_x': .5, 'center_y': .5}
                        text: str(root.waterback)
                        valign: 'center'
                            
                        MDTextFieldHintText:
                            text: 'текущий'
                
                MDWidget:
                    size_hint_x: 1
                    size_hint_y: None
                    
                MDButton:
                    style: 'tonal'
                    pos_hint: {'top_x': 0.5, 'top_y': 0.5}
                    on_release: root.saveconf()
                    
                    MDButtonIcon:
                        icon: 'content-save-settings'
                        
                    MDButtonText:
                        text: 'Сохранить'
                    
            
"""


def error():
    """Открытие окна ошибки
    Вызывается при введении некорректных данных в поле ввода тарифов
    MDTextField расположенных в MDNavigationDrawer
    
    """

    def errorclose(self):
        """Закрывает окно ошибки"""
        dialogerror.dismiss()
        return

    dialogerror = MDDialog(
        # ---- Headline text -----
        MDDialogHeadlineText(
            text='Ошибка',
            halign='center',
        ),
        # ---- Support text ----
        MDDialogSupportingText(
            text='Введите стоимость в числовом формате.',
        ),
        #  ---- Button container ----
        MDDialogButtonContainer(
            MDButton(
                MDButtonText(
                    text='Ok',
                ),
                on_release=errorclose
            )
        )
    )
    dialogerror.open()
    return


class MainScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # считывание БД со значениями тарифов
        self.prices = pd.read_csv('prices.csv', index_col=0)
        # значения переменных присваиваются из БД
        self.cwaterprice = self.prices.loc['cwaterprice', 'price']
        self.gcalprice = self.prices.loc['gcalprice', 'price']
        self.waterback = self.prices.loc['waterback', 'price']

    def calculation(self):
        """Функция основных калькуляций

        Расчет показателей, вывод параметров расчета на экран в ~ids.label_out (str)
        """
        try:
            self.cold_water = float(self.ids.cold_label.text)
            self.hot_water = float(self.ids.hot_label.text)
        
            hw = self.hot_water
            hws_nositel = round(hw * self.cwaterprice, 2)
            hws_energy = round(hw * 0.0649 * self.gcalprice, 2)
            hw_result = round(hws_nositel + hws_energy, 2)
            cw_result = round(self.cold_water * self.cwaterprice, 2)
            water_out = round((self.cold_water + self.hot_water) * self.waterback, 2)
            water_result = round(hw_result + cw_result + water_out, 2)
            self.ids.w_result_label.text = str(water_result)

            # вывод промежуточные расчеты на экран в label_out
            self.ids.label_out.text = 'Тариф ХВ - ' + str(self.cwaterprice) + ' руб/м[sup]3[/sup]' \
                + '\nТариф на тепл. эн. - ' + str(self.gcalprice) + ' руб/Гкал' \
                + '\nТариф на водоотведение - ' + str(self.waterback) + ' руб/м[sup]3[/sup]' \
                + '\nГВС носитель - ' + str(hws_nositel) + ' руб.'\
                + '\nГВС энергия - ' + str(hws_energy) + ' руб.'\
                + '\nГВ сумм - ' + str(hw_result) + ' руб.'\
                + '\nХВ сумм - ' + str(cw_result) + ' руб.'\
                + '\nВодоотведение - ' + str(water_out) + ' руб.'

        except Exception as e:
            print(e)
        return 
       
    def saveconf(self):
        """Сохранение данных о тарифах

        Обновляет значения переменных
        self.cwaterprice (float)
        self.gcalprice (float)
        self.waterback (float)

        Вносит изменения в self.prices (DataFrame)
        Сохраняет данные в файл prices.csv
        """
        try:
            self.cwaterprice = float(self.ids.cwaterprice.text)
            self.gcalprice = float(self.ids.gcalprice.text)
            self.waterback = float(self.ids.waterback.text)
            
            # обновление значений в ячейках БД, с округлением до 2-го знака
            self.prices.loc['cwaterprice', 'price'] = round(self.cwaterprice, 2)
            self.prices.loc['gcalprice', 'price'] = round(self.gcalprice, 2)
            self.prices.loc['waterback', 'price'] = round(self.waterback, 2)

            # сохранение значений цен в отдельный файл
            self.prices.to_csv('prices.csv')

            # df = pd.DataFrame([[self.cwaterprice],
            #                    [self.gcalprice],
            #                    [self.waterback]],
            #                   dtype=float,
            #                   index=['cwaterprice', 'gcalprice', 'waterback'],
            #                   columns=['price'])
            # df.to_csv('prices.csv')

        except ValueError:
            error()

        return


class HotColdWaterBill(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Blue'
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main_screen'))
        return Builder.load_string(KV)

    def set_dynamic_color(self):
        self.theme_cls.dynamic_color = True


if __name__ == "__main__":                    
    HotColdWaterBill().run()
