### ripgrep
```log
PS G:\GGames\Minecraft\aaaSERVERSaaa\aaa_from_git_aaa\github\MCDReforged> rg -i rtext 
tests\test_translation.py
9:from mcdreforged.minecraft.rtext.text import RText, RTextBase
48:             rtext = tr('key1', ('X', RText('Y')), {'c': 'Z'})
49:             self.assertIsInstance(rtext, RTextBase)
50:             self.assertEqual('A X bb Z Yzzz', rtext.to_plain_text())
51:             self.assertEqual(4, len(rtext.to_json_object()))
53:             rtext = tr('key1', ('X', RText('Y')), {'c': RText('Z')})
54:             self.assertIsInstance(rtext, RTextBase)
55:             self.assertEqual('A X bb Z Yzzz', rtext.to_plain_text())

tests\rtext\test_rtext.py
5:from mcdreforged.api.rtext import *
8:class RTextComponentTestCase(unittest.TestCase):
10:             self.assertEqual('foo', RText('foo').to_plain_text())
11:             self.assertEqual('foo', RText('foo', RColor.red).to_plain_text())
12:             self.assertEqual('foo', RText('foo', RColor.red, RStyle.bold).to_plain_text())
14:             text = RTextList('foo', RText('bar', RColor.yellow), 'baz')
20:             self.assertEqual('foo', RText('foo').to_colored_text())
21:             self.assertEqual(Fore.LIGHTRED_EX + 'foo' + Style.RESET_ALL, RText('foo', RColor.red).to_colored_text())
22:             self.assertEqual(Fore.LIGHTRED_EX + Style.BRIGHT + 'foo' + Style.RESET_ALL, RText('foo', RColor.red, RStyle.bold).to_colored_text())
24:             text = RTextList('foo', RText('bar', RColor.yellow), 'baz')
35:             self.assertEqual('foo', RText('foo').to_legacy_text())
36:             self.assertEqual('§c' + 'foo' + '§r', RText('foo', RColor.red).to_legacy_text())
37:             self.assertEqual('§c§l' + 'foo' + '§r', RText('foo', RColor.red, RStyle.bold).to_legacy_text())
39:             text = RTextList('foo', RText('bar', RColor.yellow), 'baz')

mcdreforged\mcdr_server.py
238:            If args contains RText element, then the result will be a RText, otherwise the result will be a regular str
316:            self.logger.info(future.result().to_rtext(self, show_path=True))

tests\rtext\test_rstyle.py
3:from mcdreforged.api.rtext import *
6:class RTextColorTestCase(unittest.TestCase):
60:class RTextStyleTestCase(unittest.TestCase):

tests\rtext\test_hover_event.py
6:from mcdreforged import RHoverText, RText, RHoverAction, RColor, RHoverEntity, RHoverEvent, RTextJsonFormat, RHoverItem
9:class RTextColorTestCase(unittest.TestCase):
13:             self.assertEqual(hover_event.to_json_object(RTextJsonFormat.V_1_7), json_1_7)
14:             self.assertEqual(hover_event.to_json_object(RTextJsonFormat.V_1_21_5), json_1_21_5)
16:             verifier(RHoverEvent.from_json_object(json_1_7, RTextJsonFormat.V_1_7))
17:             verifier(RHoverEvent.from_json_object(json_1_16, RTextJsonFormat.V_1_7))
18:             verifier(RHoverEvent.from_json_object(json_1_21_5, RTextJsonFormat.V_1_21_5))
22:                     self.assertIsInstance(he, RHoverText)
26:             text = RText('foo', color=RColor.red)
28:                     RHoverText(text=text),
50:                     self.assertEqual(he.name, RText('custom name'))
56:                             name=RText('custom name'),
93:                     }, RTextJsonFormat.V_1_21_5)
137:    def test_3_rtext_api(self):
138:            text = RText('foo')
143:            text.set_hover_event(RHoverText(text=RText('bar')))
144:            self.assertEqual(text.to_json_object(json_format=RTextJsonFormat.V_1_7), js_1_7)
145:            self.assertEqual(text.to_json_object(json_format=RTextJsonFormat.V_1_21_5), js_1_21_5)
147:            self.assertEqual(text, RText('foo').set_hover_text(RText('bar')))
148:            self.assertEqual(text, RText('foo').h(RText('bar')))

docs\static\js\algolia.js
98:switchgear.innerText = algolia_enabled ? switchgear_tr.disable : switchgear_tr.enable;

mcdreforged\logging\formatter.py
9:from mcdreforged.minecraft.rtext.style import RItemClassic, RColor, RStyle

tests\rtext\test_click_event.py
4:from mcdreforged import RText, RClickAction, RClickSuggestCommand, RTextJsonFormat, RClickEvent, RClickRunCommand, RClickOpenUrl, RClickCopyToClipboard, RClickOpenFile
5:from mcdreforged.minecraft.rtext.click_event import RClickChangePage, RClickShowDialog, RClickCustom
8:class RTextColorTestCase(unittest.TestCase):
13:                     self.assertEqual(click_event.to_json_object(RTextJsonFormat.V_1_7), json_1_7)
15:                     click_event.to_json_object(RTextJsonFormat.V_1_7)  # just don't crash
16:             self.assertEqual(click_event.to_json_object(RTextJsonFormat.V_1_21_5), json_1_21_5)
19:                     verifier(RClickEvent.from_json_object(json_1_7, RTextJsonFormat.V_1_7))
20:             verifier(RClickEvent.from_json_object(json_1_21_5, RTextJsonFormat.V_1_21_5))
127:    def test_8_rtext_api(self):
128:            text = RText('foo')
134:            self.assertEqual(text.to_json_object(json_format=RTextJsonFormat.V_1_7), js_1_7)
135:            self.assertEqual(text.to_json_object(json_format=RTextJsonFormat.V_1_21_5), js_1_21_5)
137:            self.assertEqual(text, RText('foo').set_click_event(RClickSuggestCommand('/say something')))
138:            self.assertEqual(text, RText('foo').set_click_event(event=RClickSuggestCommand('/say something')))
139:            self.assertEqual(text, RText('foo').set_click_event(RClickAction.suggest_command, '/say something'))
140:            self.assertEqual(text, RText('foo').set_click_event(action=RClickAction.suggest_command, value='/say something'))
141:            self.assertEqual(text, RText('foo').c(RClickSuggestCommand('/say something')))
142:            self.assertEqual(text, RText('foo').c(RClickAction.suggest_command, '/say something'))

mcdreforged\utils\types\message.py
4:      from mcdreforged.minecraft.rtext.text import RTextBase
7:MessageText = Union[str, 'RTextBase']

docs\source\migrate\1.x_to_2.x.rst
17:You can no longer use :class:`RText <mcdreforged.minecraft.rtext.text.RTextBase>` instance as the value of your plugin metadata. 
18:``name`` and ``description`` fields in :class:`RText <mcdreforged.minecraft.rtext.text.RTextBase>` class will be automatically converted into ``str`` for compatibility

docs\source\plugin_dev\dev_tips.rst
42:* :meth:`~mcdreforged.plugin.si.server_interface.ServerInterface.rtr`, or :class:`~mcdreforged.translation.translation_text.RTextMCDRTranslation` is ``new TranslatableText()``

mcdreforged\handler\impl\abstract_minecraft_handler.py
13:from mcdreforged.minecraft.rtext.text import RTextBase, RTextJsonFormat
63:def _get_rtext_json_format(version_name: Optional[str]) -> RTextJsonFormat:
66:             return RTextJsonFormat.V_1_21_5
68:             return RTextJsonFormat.default()
114:            if isinstance(message, RTextBase):
115:                    json_format = _get_rtext_json_format(server_information.version) if server_information else RTextJsonFormat.default()

docs\source\migrate\0.x_to_1.x.rst
138:If your plugin imports some of the mcdr utils, like ``RText`` or ``Rcon``\ , you need to take a look at the package location
142:Use ``from mcdreforged.api.rtext import *`` if you want to use all rtext classes

docs\source\plugin_dev\api.rst
121:rtext
124:Module path: ``mcdreforged.api.rtext``
130:Inspired by the `MCD stext API <https://github.com/TISUnion/rtext>`__ made by `Pandaria98 <https://github.com/Pandaria98>`__
132:Class references: :ref:`code_references/minecraft_tools:RText`

mcdreforged\handler\impl\beta18_handler.py
9:from mcdreforged.minecraft.rtext.text import RTextBase
21:             if isinstance(message, RTextBase):

mcdreforged\utils\text_utils.py
41:             from mcdreforged.minecraft.rtext.style import RStyle
42:             from mcdreforged.minecraft.rtext.text import RTextBase
48:                                     cell = RTextBase.from_any(cell).set_styles(RStyle.bold)
53:                     lines.append(RTextBase.join('   ', items))

mcdreforged\executor\update_helper.py
15:from mcdreforged.minecraft.rtext.click_event import RAction
16:from mcdreforged.minecraft.rtext.style import RColor, RStyle
17:from mcdreforged.minecraft.rtext.text import RText
64:                                                     RText(err_doc_url, color=RColor.blue, styles=RStyle.underlined).

docs\source\code_references\minecraft_tools.rst
5:RText
8::doc:`API package </plugin_dev/api>` path: ``mcdreforged.api.rtext``
10:.. automodule:: mcdreforged.minecraft.rtext
15:.. currentmodule:: mcdreforged.minecraft.rtext.style
47:.. automodule:: mcdreforged.minecraft.rtext.click_event
53:.. automodule:: mcdreforged.minecraft.rtext.hover_event
59:.. currentmodule:: mcdreforged.minecraft.rtext.text
61:.. autoclass:: RTextBase
64:.. autoclass:: RText
69:.. autoclass:: RTextList
74:.. autoclass:: RTextTranslation
79:.. autoclass:: mcdreforged.translation.translation_text.RTextMCDRTranslation
87:.. autoclass:: mcdreforged.minecraft.rtext.schema.RTextJsonFormat

mcdreforged\translation\translator.py
8:      from mcdreforged.translation.translation_text import RTextMCDRTranslation
18:             from mcdreforged.translation.translation_text import RTextMCDRTranslation
19:             self.__rtr_cls = RTextMCDRTranslation
33:     def __call__(self, key: str, *args, **kwargs) -> 'RTextMCDRTranslation':

docs\source\_locale\zh_CN\LC_MESSAGES\plugin_dev\dev_tips.po
102:":class:`~mcdreforged.translation.translation_text.RTextMCDRTranslation` "
106:":class:`~mcdreforged.translation.translation_text.RTextMCDRTranslation` "

mcdreforged\plugin\operation_result.py
7:from mcdreforged.minecraft.rtext.click_event import RAction
8:from mcdreforged.minecraft.rtext.text import RTextList, RTextBase
95:     def to_rtext(self, mcdr_server: 'MCDReforgedServer', *, show_path: bool) -> RTextBase:
96:             def add_element(msg: RTextList, element):
102:            def add_if_not_empty(msg: RTextList, lst: list, key: str):
112:            message = RTextList()

docs\source\_locale\zh_CN\LC_MESSAGES\code_references\ServerInterface.po
221:"If args or kwargs contains :class:`RText "
222:"<mcdreforged.minecraft.rtext.text.RTextBase>` element, then the result "
223:"will be a :class:`RText <mcdreforged.minecraft.rtext.text.RTextBase>`, "
226:"如果 args 或者 kwargs 包含 :class:`RText "
227:"<mcdreforged.minecraft.rtext.text.RTextBase>` 元素，则结果将为一个 :class:`RText "
228:"<mcdreforged.minecraft.rtext.text.RTextBase>`，否则结果将是一个 str"
271:":class:`~mcdreforged.translation.translation_text.RTextMCDRTranslation` "
276:":class:`~mcdreforged.translation.translation_text.RTextMCDRTranslation` "
290:":class:`~mcdreforged.translation.translation_text.RTextMCDRTranslation` "
294:":class:`~mcdreforged.translation.translation_text.RTextMCDRTranslation`"

docs\source\_locale\zh_CN\LC_MESSAGES\code_references\minecraft_tools.po
22:msgid "RText"
23:msgstr "RText"
26:msgid ":doc:`API package </plugin_dev/api>` path: ``mcdreforged.api.rtext``"
27:msgstr ":doc:`API  包 </plugin_dev/api>` 路径: ``mcdreforged.api.rtext``"
29:#: mcdreforged.minecraft.rtext:1 of
33:#: mcdreforged.minecraft.rtext:3 of
45:#: mcdreforged.minecraft.rtext.style.RItem:1 of
49:#: mcdreforged.minecraft.rtext.style.RItem.name:1 of
53:#: mcdreforged.minecraft.rtext.style.RItemClassic:1 of
55:"Bases: :py:class:`~mcdreforged.minecraft.rtext.style.RItem`, "
59:#: mcdreforged.minecraft.rtext.style.RItemClassic:1 of
68:#: mcdreforged.minecraft.rtext.style.RItemClassic:4 of
77:#: mcdreforged.minecraft.rtext.style.RItemClassic.mc_code:1 of
81:#: mcdreforged.minecraft.rtext.style.RItemClassic.console_code:1 of
85:#: mcdreforged.minecraft.rtext.style.RItemClassic.console_code:3 of
89:#: mcdreforged.minecraft.rtext.style.RColor:1 of
93:#: mcdreforged.minecraft.rtext.style.RColor.from_mc_value:1 of
103:#: mcdreforged.minecraft.rtext.style.RColor.from_mc_value:3 of
113:#: mcdreforged.minecraft.rtext.style.RColor.from_mc_value:5 of
121:#: mcdreforged.minecraft.rtext.style.RColor.from_mc_value:6 of
125:#: mcdreforged.minecraft.rtext.style.RColor.r:1 of
129:#: mcdreforged.minecraft.rtext.style.RColor.g:1 of
133:#: mcdreforged.minecraft.rtext.style.RColor.b:1 of
137:#: mcdreforged.minecraft.rtext.style.RColorClassic:1 of
139:"Bases: :py:class:`~mcdreforged.minecraft.rtext.style.RItemClassic`, "
140:":py:class:`~mcdreforged.minecraft.rtext.style.RColor`"
143:#: mcdreforged.minecraft.rtext.style.RColorClassic:1 of
147:#: mcdreforged.minecraft.rtext.style.RColorClassic:5 of
153:#: mcdreforged.minecraft.rtext.style.RColorClassic.to_rgb:1 of
159:#: mcdreforged.minecraft.rtext.style.RColorRGB:1 of
165:#: mcdreforged.minecraft.rtext.style.RColorRGB:4 of
169:#: mcdreforged.minecraft.rtext.style.RColorRGB.__init__:1
170:#: mcdreforged.minecraft.rtext.style.RColorRGB.from_code:3 of
178:#: mcdreforged.minecraft.rtext.style.RColorRGB.from_code:1 of
184:#: mcdreforged.minecraft.rtext.style.RColorRGB.from_rgb:1 of
190:#: mcdreforged.minecraft.rtext.style.RColorRGB.from_rgb:3 of
194:#: mcdreforged.minecraft.rtext.style.RColorRGB.from_rgb:4 of
198:#: mcdreforged.minecraft.rtext.style.RColorRGB.from_rgb:5 of
202:#: mcdreforged.minecraft.rtext.style.RColorRGB.to_classic:1 of
208:#: mcdreforged.minecraft.rtext.style.RStyle:1 of
212:#: mcdreforged.minecraft.rtext.style.RStyleClassic:1 of
214:"Bases: :py:class:`~mcdreforged.minecraft.rtext.style.RItemClassic`, "
215:":py:class:`~mcdreforged.minecraft.rtext.style.RStyle`"
218:#: mcdreforged.minecraft.rtext.style.RStyleClassic:1 of
228:#: mcdreforged.minecraft.rtext.click_event.RClickAction:1 of
232:#: mcdreforged.minecraft.rtext.click_event.RClickAction:4 of
239:#: mcdreforged.minecraft.rtext.click_event.RClickAction.suggest_command:1 of
244:#: mcdreforged.minecraft.rtext.click_event.RClickAction.run_command:1 of
249:#: mcdreforged.minecraft.rtext.click_event.RClickAction.run_command:3 of
260:#: mcdreforged.minecraft.rtext.click_event.RClickAction.run_command:8 of
270:#: mcdreforged.minecraft.rtext.click_event.RClickAction.run_command:10 of
277:#: mcdreforged.minecraft.rtext.click_event.RClickAction.run_command:12 of
282:#: mcdreforged.minecraft.rtext.click_event.RClickAction.open_url:1 of
287:#: mcdreforged.minecraft.rtext.click_event.RClickAction.open_file:1 of
292:#: mcdreforged.minecraft.rtext.click_event.RClickAction.open_file:5 of
302:#: mcdreforged.minecraft.rtext.click_event.RClickAction.copy_to_clipboard:1 of
307:#: mcdreforged.minecraft.rtext.click_event.RClickAction.copy_to_clipboard:3 of
312:#: mcdreforged.minecraft.rtext.click_event.RClickAction.change_page:1 of
317:#: mcdreforged.minecraft.rtext.click_event.RClickAction.change_page:3 of
322:#: mcdreforged.minecraft.rtext.click_event.RClickAction.show_dialog:1 of
327:#: mcdreforged.minecraft.rtext.click_event.RClickAction.custom:3
328:#: mcdreforged.minecraft.rtext.click_event.RClickAction.show_dialog:3
329:#: mcdreforged.minecraft.rtext.click_event.RClickCustom:3
330:#: mcdreforged.minecraft.rtext.click_event.RClickShowDialog:3 of
335:#: mcdreforged.minecraft.rtext.click_event.RClickAction.custom:1 of
339:#: mcdreforged.minecraft.rtext.click_event.RClickAction:1 of
343:#: mcdreforged.minecraft.rtext.click_event.RClickEvent:1 of
347:#: mcdreforged.minecraft.rtext.click_event.RClickEvent.action:1 of
351:#: mcdreforged.minecraft.rtext.click_event.RClickEvent.to_json_object:1
352:#: mcdreforged.minecraft.rtext.hover_event.RHoverEvent.to_json_object:1 of
356:#: mcdreforged.minecraft.rtext.click_event.RClickEvent.to_json_object:3
357:#: mcdreforged.minecraft.rtext.hover_event.RHoverEvent.to_json_object:3 of
361:#: mcdreforged.minecraft.rtext.click_event.RClickEvent.from_json_object:1 of
365:#: mcdreforged.minecraft.rtext.click_event.RClickEvent.from_json_object:3
366:#: mcdreforged.minecraft.rtext.hover_event.RHoverEvent.from_json_object:3 of
370:#: mcdreforged.minecraft.rtext.click_event.RClickEvent.from_json_object:4
371:#: mcdreforged.minecraft.rtext.hover_event.RHoverEvent.from_json_object:4 of
375:#: mcdreforged.minecraft.rtext.click_event.RClickEventSingleValue:1 of
381:#: mcdreforged.minecraft.rtext.click_event.RClickSuggestCommand:1 of
386:#: mcdreforged.minecraft.rtext.click_event.RClickSuggestCommand.command:1 of
390:#: mcdreforged.minecraft.rtext.click_event.RClickRunCommand:1 of
395:#: mcdreforged.minecraft.rtext.click_event.RClickRunCommand.command:1 of
399:#: mcdreforged.minecraft.rtext.click_event.RClickOpenUrl:1 of
403:#: ../../docstring mcdreforged.minecraft.rtext.click_event.RClickOpenUrl.url:1
408:#: mcdreforged.minecraft.rtext.click_event.RClickOpenFile:1 of
413:#: mcdreforged.minecraft.rtext.click_event.RClickOpenFile.path:1 of
417:#: mcdreforged.minecraft.rtext.click_event.RClickCopyToClipboard:1 of
424:#: mcdreforged.minecraft.rtext.click_event.RClickCopyToClipboard.value:1 of
428:#: mcdreforged.minecraft.rtext.click_event.RClickShowDialog:1 of
433:#: mcdreforged.minecraft.rtext.click_event.RClickShowDialog.dialog:1 of
438:#: mcdreforged.minecraft.rtext.click_event.RClickShowDialog.dialog:3 of
443:#: mcdreforged.minecraft.rtext.click_event.RClickShowDialog.dialog:4 of
447:#: mcdreforged.minecraft.rtext.click_event.RClickChangePage:1 of
452:#: mcdreforged.minecraft.rtext.click_event.RClickChangePage.page:1 of
456:#: mcdreforged.minecraft.rtext.click_event.RClickCustom:1 of
460:#: ../../docstring mcdreforged.minecraft.rtext.click_event.RClickCustom.id:1 of
465:#: mcdreforged.minecraft.rtext.click_event.RClickCustom.payload:1 of
473:#: mcdreforged.minecraft.rtext.hover_event.RHoverAction:1 of
478:#: mcdreforged.minecraft.rtext.hover_event.RHoverAction.show_text:1 of
483:#: mcdreforged.minecraft.rtext.hover_event.RHoverAction.show_entity:1 of
488:#: mcdreforged.minecraft.rtext.hover_event.RHoverAction.show_item:1 of
492:#: mcdreforged.minecraft.rtext.hover_event.RHoverEvent:1 of
496:#: mcdreforged.minecraft.rtext.hover_event.RHoverEvent.action:1 of
500:#: mcdreforged.minecraft.rtext.hover_event.RHoverEvent.from_json_object:1 of
504:#: mcdreforged.minecraft.rtext.hover_event.RHoverText:1 of
508:#: ../../docstring mcdreforged.minecraft.rtext.hover_event.RHoverText.text:1 of
512:#: mcdreforged.minecraft.rtext.hover_event.RHoverEntity:1 of
516:#: ../../docstring mcdreforged.minecraft.rtext.hover_event.RHoverEntity.id:1 of
520:#: ../../docstring mcdreforged.minecraft.rtext.hover_event.RHoverEntity.uuid:1
525:#: ../../docstring mcdreforged.minecraft.rtext.hover_event.RHoverEntity.name:1
530:#: mcdreforged.minecraft.rtext.hover_event.RHoverItem:1 of
534:#: ../../docstring mcdreforged.minecraft.rtext.hover_event.RHoverItem.id:1 of
538:#: ../../docstring mcdreforged.minecraft.rtext.hover_event.RHoverItem.count:1
546:#: mcdreforged.minecraft.rtext.hover_event.RHoverItem.components:1 of
554:#: mcdreforged.minecraft.rtext.text.RTextBase:1 of
558:#: mcdreforged.minecraft.rtext.text.RTextBase.to_json_object:1 of
564:#: mcdreforged.minecraft.rtext.text.RTextBase.to_json_str:1 of
568:#: mcdreforged.minecraft.rtext.text.RTextBase.to_json_str:3 of
574:#: mcdreforged.minecraft.rtext.text.RTextBase.to_plain_text:1 of
578:#: mcdreforged.minecraft.rtext.text.RTextBase.to_colored_text:3
579:#: mcdreforged.minecraft.rtext.text.RTextBase.to_legacy_text:3
580:#: mcdreforged.minecraft.rtext.text.RTextBase.to_plain_text:3 of
584:#: mcdreforged.minecraft.rtext.text.RTextBase.to_colored_text:1 of
588:#: mcdreforged.minecraft.rtext.text.RTextBase.to_legacy_text:1 of
594:#: mcdreforged.minecraft.rtext.text.RTextBase.copy:1 of
598:#: mcdreforged.minecraft.rtext.text.RTextBase.set_color:1 of
602:#: mcdreforged.minecraft.rtext.text.RTextBase.set_styles:1 of
606:#: mcdreforged.minecraft.rtext.text.RTextBase.set_click_event:1 of
610:#: mcdreforged.minecraft.rtext.text.RTextBase.set_click_event:3 of
616:#: mcdreforged.minecraft.rtext.text.RTextBase.set_click_event:12 of
620:#: mcdreforged.minecraft.rtext.text.RTextBase.set_hover_event:1 of
624:#: mcdreforged.minecraft.rtext.text.RTextBase.set_hover_text:1 of
628:#: mcdreforged.minecraft.rtext.text.RTextBase.set_hover_text:3 of
632:#: mcdreforged.minecraft.rtext.text.RTextBase.set_hover_text:5 of
634:"The elements be used to create a :class:`RTextList` instance. The "
635:":class:`RTextList` instance is used as the actual hover text"
636:msgstr "用于创建 :class:`RTextList` 实例的元素。:class:`RTextList` 实例将作为实际的悬浮文本"
638:#: mcdreforged.minecraft.rtext.text.RTextBase.set_hover_text:7 of
642:#: mcdreforged.minecraft.rtext.text.RTextBase.set_click_event:1 of
646:#: mcdreforged.minecraft.rtext.text.RTextBase.set_hover_text:1 of
650:#: mcdreforged.minecraft.rtext.text.RTextBase.from_any:1 of
651:msgid "Convert anything into a RText component"
652:msgstr "将任意对象转换为一个 RText 组件"
654:#: mcdreforged.minecraft.rtext.text.RTextBase.join:1 of
660:#: mcdreforged.minecraft.rtext.text.RTextBase.format:3
661:#: mcdreforged.minecraft.rtext.text.RTextBase.from_json_object:3
662:#: mcdreforged.minecraft.rtext.text.RTextBase.join:3
663:#: mcdreforged.minecraft.rtext.text.RTextTranslation.__init__:6
664:#: mcdreforged.translation.translation_text.RTextMCDRTranslation.language_context:8
669:#: mcdreforged.minecraft.rtext.text.RTextBase.join:9 of
673:#: mcdreforged.minecraft.rtext.text.RTextBase.join:10 of
677:#: mcdreforged.minecraft.rtext.text.RTextBase.format:1 of
680:" to build a formatted RText component based on the formatter *fmt*"
683:"的基础上进行格式化并生成一个 RText 组件"
685:#: mcdreforged.minecraft.rtext.text.RTextBase.format:9 of
689:#: mcdreforged.minecraft.rtext.text.RTextBase.format:10 of
693:#: mcdreforged.minecraft.rtext.text.RTextBase.format:11 of
697:#: mcdreforged.minecraft.rtext.text.RTextBase.from_json_object:1 of
698:msgid "Convert a json object into a :class:`RText <RTextBase>` component"
699:msgstr "将一个 json 对象转换为一个 :class:`RText <RTextBase>` 组件"
701:#: mcdreforged.minecraft.rtext.text.RTextBase.from_json_object:11 of
705:#: mcdreforged.minecraft.rtext.text.RText:1
706:#: mcdreforged.minecraft.rtext.text.RTextList:1
707:#: mcdreforged.translation.translation_text.RTextMCDRTranslation:1 of
708:msgid "Bases: :py:class:`~mcdreforged.minecraft.rtext.text.RTextBase`"
711:#: mcdreforged.minecraft.rtext.text.RText:1 of
715:#: mcdreforged.minecraft.rtext.text.RText.__init__:1 of
717:"Create a :class:`RText` object with specific text, optional color and "
719:msgstr "给定文本创建一个 :class:`RText` 对象，可选文本颜色及样式"
721:#: mcdreforged.minecraft.rtext.text.RText.__init__:3 of
725:#: mcdreforged.minecraft.rtext.text.RText.__init__:4
726:#: mcdreforged.minecraft.rtext.text.RTextTranslation.__init__:11 of
730:#: mcdreforged.minecraft.rtext.text.RText.__init__:5 of
733:":class:`~mcdreforged.minecraft.rtext.style.RStyle` or an iterable of "
734:":class:`~mcdreforged.minecraft.rtext.style.RStyle`"
737:":class:`~mcdreforged.minecraft.rtext.style.RStyle`，也可以是 "
738:":class:`~mcdreforged.minecraft.rtext.style.RStyle` 的一个可迭代对象"
740:#: mcdreforged.minecraft.rtext.text.RTextList:1 of
741:msgid "A list of :class:`RTextBase` objects, a compound text component"
742:msgstr "一个储存着若干个 :class:`RTextBase` 对象的列表，即一个复合文本组件"
744:#: mcdreforged.minecraft.rtext.text.RTextList.__init__:1 of
745:msgid "Use the given *\\*args* to create a :class:`RTextList`"
746:msgstr "使用给定的 *\\*args* 创建一个 :class:`RTextList`"
748:#: mcdreforged.minecraft.rtext.text.RTextList.__init__:3 of
750:"The items in this :class:`RTextList`. They can be :class:`str`, "
751:":class:`RTextBase` or any class implements ``__str__`` method. All non- "
752:":class:`RTextBase` items will be converted to :class:`RText`"
754:"此 :class:`RTextList` 中的元素。它们可以是 :class:`str`，:class:`RTextBase` 或任何实现了 "
755:"``__str__`` 方法的类。所有的非 :class:`RTextBase` 元素都将被转换为 :class:`RText`"
757:#: mcdreforged.minecraft.rtext.text.RTextTranslation:1 of
758:msgid "Bases: :py:class:`~mcdreforged.minecraft.rtext.text.RText`"
761:#: mcdreforged.minecraft.rtext.text.RTextTranslation:1 of
764:":class:`RText`"
765:msgstr "翻译文本组件类。几乎和 :class:`RText` 相同"
767:#: mcdreforged.minecraft.rtext.text.RTextTranslation.__init__:1 of
769:"Create a :class:`RTextTranslation` object with specific translation key. "
771:":class:`RText`"
772:msgstr "使用特定的翻译键创建一个 :class:`RTextTranslation` 对象。其余参数与 :class:`RText` 相同"
774:#: mcdreforged.minecraft.rtext.text.RTextTranslation.__init__:4 of
780:#: mcdreforged.minecraft.rtext.text.RTextTranslation.__init__:10
781:#: mcdreforged.translation.translation_text.RTextMCDRTranslation.__init__:3 of
785:#: mcdreforged.minecraft.rtext.text.RTextTranslation.__init__:12 of
788:":class:`~mcdreforged.minecraft.rtext.style.RStyle` or a collection of "
789:":class:`~mcdreforged.minecraft.rtext.style.RStyle`"
792:":class:`~mcdreforged.minecraft.rtext.style.RStyle`，也可以是 "
793:":class:`~mcdreforged.minecraft.rtext.style.RStyle` 的一个可迭代对象"
795:#: mcdreforged.minecraft.rtext.text.RTextTranslation.arg:1 of
799:#: mcdreforged.minecraft.rtext.text.RTextTranslation.arg:3
800:#: mcdreforged.translation.translation_text.RTextMCDRTranslation.__init__:4 of
804:#: mcdreforged.minecraft.rtext.text.RTextTranslation.fallback:1 of
808:#: mcdreforged.minecraft.rtext.text.RTextTranslation.fallback:5 of
812:#: mcdreforged.minecraft.rtext.text.RTextTranslation.fallback:7 of
816:#: mcdreforged.translation.translation_text.RTextMCDRTranslation:1 of
820:#: mcdreforged.translation.translation_text.RTextMCDRTranslation:3 of
833:#: mcdreforged.translation.translation_text.RTextMCDRTranslation.__init__:1 of
835:"Create a :class:`RTextMCDRTranslation` component with necessary "
837:msgstr "使用与翻译相关的必要参数创建一个 :class:`RTextMCDRTranslation` 组件"
839:#: mcdreforged.translation.translation_text.RTextMCDRTranslation.__init__:5 of
843:#: mcdreforged.translation.translation_text.RTextMCDRTranslation.language_context:1
846:"Create a context where all :class:`RTextMCDRTranslation` will use the "
848:msgstr "创建一个上下文，在其中所有的 :class:`RTextMCDRTranslation` 将会使用给定的语言来进行翻译"
850:#: mcdreforged.translation.translation_text.RTextMCDRTranslation.language_context:3
857:#: mcdreforged.translation.translation_text.RTextMCDRTranslation.language_context:5
865:#: mcdreforged.translation.translation_text.RTextMCDRTranslation.language_context:19
874:#: mcdreforged.minecraft.rtext.schema.RTextJsonFormat:1 of
876:"Define the serialization format of :class:`RText <RTextBase>` components "
878:msgstr "为不同的 Minecraft 版本定义的 :class:`RText <RTextBase>` 组件的序列化格式"
880:#: ../../docstring mcdreforged.minecraft.rtext.schema.RTextJsonFormat.V_1_7:1
886:#: mcdreforged.minecraft.rtext.schema.RTextJsonFormat.V_1_21_5:1 of

docs\source\_locale\zh_CN\LC_MESSAGES\plugin_dev\api.po
200:msgid "rtext"
201:msgstr "rtext"
204:msgid "Module path: ``mcdreforged.api.rtext``"
205:msgstr "模块路径: ``mcdreforged.api.rtext``"
223:"Inspired by the `MCD stext API <https://github.com/TISUnion/rtext>`__ "
227:"<https://github.com/TISUnion/rtext>`__ 的启发，在此表达感谢"
230:msgid "Class references: :ref:`code_references/minecraft_tools:RText`"
231:msgstr "类参考：:ref:`code_references/minecraft_tools:RText`"

mcdreforged\utils\replier.py
48:             from mcdreforged.minecraft.rtext.text import RTextBase
49:             if isinstance(message, RTextBase):

mcdreforged\plugin\installer\downloader.py
14:from mcdreforged.minecraft.rtext.style import RColor
15:from mcdreforged.minecraft.rtext.text import RText, RTextList
26:                     return RText(result) + RText('...', color=RColor.gray)
111:                    simple_msg = RTextList(file_name, ' ', percent_str)
112:                    simple_msg_m = RTextList(file_name, ' ', percent_str_m)
127:                            self.replier.reply(RTextList(file_name, f' [{bar}] {percent_str}'))

mcdreforged\minecraft\rtext\text.py
9:from mcdreforged.minecraft.rtext.click_event import RClickAction, RClickEvent, RClickEventSingleValue
10:from mcdreforged.minecraft.rtext.hover_event import RHoverEvent, RHoverText
11:from mcdreforged.minecraft.rtext.schema import RTextJsonFormat
12:from mcdreforged.minecraft.rtext.style import RStyle, RColor, RColorClassic, RColorRGB, RItemClassic
25:class RTextBase(ABC):
31:             json_format: NotRequired[RTextJsonFormat]
34:             json_format: NotRequired[Optional[RTextJsonFormat]]  # None means auto-detect
147:                    text = RText('example')
192:            :param args: The elements be used to create a :class:`RTextList` instance.
193:                    The :class:`RTextList` instance is used as the actual hover text
202:                    text = RTextBase.from_any(args[0])
204:                    text = RTextList(*args)
205:            self.set_hover_event(RHoverText(text=text))
222:            return RTextList(self, other)
225:            return RTextList(other, self)
228:    def from_any(text) -> 'RTextBase':
230:            Convert anything into a RText component
232:            if isinstance(text, RTextBase):
234:            return RText(text)
237:    def join(divider: Any, iterable: Iterable[Any]) -> 'RTextBase':
243:                    >>> text = RTextBase.join(',', [RText('1'), '2', 3])
250:            result = RTextList()
258:    def format(fmt: str, *args, **kwargs) -> 'RTextBase':
260:            Just like method :meth:`str.format`, it uses *\\*args* and *\\*\\*kwargs* to build a formatted RText component based on the formatter *fmt*
264:                    >>> text = RTextBase.format('a={},b={},c={c}', RText('1', color=RColor.blue), '2', c=3)
275:            rtext_elements: List[Tuple[str, RTextBase]] = []
279:                    ph = '@@MCDR#RText.FMT#PH#{}@@'.format(placeholder_counter)
284:                    if isinstance(arg, RTextBase):
286:                            rtext_elements.append((placeholder, arg))
289:                    if isinstance(value, RTextBase):
291:                            rtext_elements.append((placeholder, value))
294:            texts: List[Union[str, RTextBase]] = [fmt.format(*args, **kwargs)]
295:            for placeholder, rtext in rtext_elements:
296:                    new_texts: List[Union[str, RTextBase]] = []
298:                            processed_text: List[Union[str, RTextBase]] = []
302:                                                    processed_text.append(rtext)
309:            return RTextList(*texts)
312:    def __from_json_list(cls, data: list, json_format: Optional[RTextJsonFormat]) -> 'RTextBase':
313:            text = RTextList()
323:    def __from_json_dict(cls, data: dict, json_format: Optional[RTextJsonFormat]) -> 'RTextBase':
324:            text: RTextBase
326:                    text = RText(data['text'])
329:                    text = RTextTranslation(data['translate']).arg(*map(cls.from_json_object, tr_args))
331:                    raise ValueError('No method to create RText from {}'.format(data))
333:                    text_list = RTextList()
349:                    json_format = RTextJsonFormat.guess(data)
360:    def from_json_object(cls, data: Union[str, list, dict], **kwargs: Unpack[FromJsonKwargs]) -> 'RTextBase':
362:            Convert a json object into a :class:`RText <RTextBase>` component
366:                    >>> text = RTextBase.from_json_object({'text': 'my text', 'color': 'red'})
387:class RText(RTextBase):
394:            Create a :class:`RText` object with specific text, optional color and optional style
398:            :param styles: Optional, the style of the text. It can be a single :class:`~mcdreforged.minecraft.rtext.style.RStyle`
399:                    or an iterable of :class:`~mcdreforged.minecraft.rtext.style.RStyle`
438:    def to_json_object(self, **kwargs: Unpack[RTextBase.ToJsonKwargs]) -> Dict[str, Any]:
439:            json_format = kwargs.get('json_format', RTextJsonFormat.default())
498:    def copy(self) -> 'RText':
499:            copied = RText('')
528:class RTextList(RTextBase):
530:    A list of :class:`RTextBase` objects, a compound text component
535:            Use the given *\\*args* to create a :class:`RTextList`
537:            :param args: The items in this :class:`RTextList`. They can be :class:`str`, :class:`RTextBase`
538:                    or any class implements ``__str__`` method. All non- :class:`RTextBase` items
539:                    will be converted to :class:`RText`
541:            self.header: RTextBase = RText('')
543:            self.children: List[RTextBase] = []
571:    def set_header_text(self, header_text: RTextBase) -> Self:
581:    def __get_styling_header_rtext(self) -> RText:
582:            def get(text: RTextBase) -> RText:
583:                    if isinstance(text, RText):
585:                    elif isinstance(text, RTextList):
588:                            raise ValueError(f'Unexpected RTextList header text type {type(text)}')
594:                    self.children.append(RTextBase.from_any(obj))
601:    def to_json_object(self, **kwargs: Unpack[RTextBase.ToJsonKwargs]) -> Union[dict, list]:
603:            ret.extend([rtext.to_json_object(**kwargs) for rtext in self.children])
608:            return ''.join(rtext.to_plain_text() for rtext in self.children)
613:            head = self.__get_styling_header_rtext()._get_console_style_codes()
616:                    ''.join([head, rtext.to_colored_text(), tail])
617:                    for rtext in self.children
623:            head = self.__get_styling_header_rtext()._get_legacy_style_codes()
626:                    ''.join([head, rtext.to_legacy_text(), tail])
627:                    for rtext in self.children
631:    def copy(self) -> 'RTextList':
632:            copied = RTextList()
658:class RTextTranslation(RText):
660:    The translation text component class. It's almost the same as :class:`RText`
665:            Create a :class:`RTextTranslation` object with specific translation key.
666:            The rest of the parameters are the same to the constructor of :class:`RText`
672:                    RTextTranslation('advancements.nether.root.title', color=RColor.red)
676:            :param styles: Optional, the style of the text. It can be a single :class:`~mcdreforged.minecraft.rtext.style.RStyle`
677:                    or a collection of :class:`~mcdreforged.minecraft.rtext.style.RStyle`
712:    def to_json_object(self, **kwargs: Unpack[RTextBase.ToJsonKwargs]) -> Dict[str, Any]:
719:                            if isinstance(arg, RTextBase)
734:    def copy(self) -> 'RTextTranslation':
735:            copied = RTextTranslation('')

mcdreforged\translation\translation_text.py
7:from mcdreforged.minecraft.rtext.click_event import RClickEvent
8:from mcdreforged.minecraft.rtext.hover_event import RHoverEvent
9:from mcdreforged.minecraft.rtext.style import RColor, RStyle
10:from mcdreforged.minecraft.rtext.text import RTextBase, RText
16:class RTextMCDRTranslation(RTextBase):
32:             Create a :class:`RTextMCDRTranslation` component with necessary parameters for translation
41:             self.__tr_func: TranslateFunc = function_utils.always(RText(self.translation_key))
42:             self.__post_process: List[Callable[[RTextBase], Any]] = []
49:     def set_translator(self, translate_function: TranslateFunc) -> 'RTextMCDRTranslation':
54:     def from_translation_dict(cls, translation_dict: TranslationKeyMappingRich) -> 'RTextMCDRTranslation':
58:             return RTextMCDRTranslation('').set_translator(fake_tr)
60:     def __get_translated_text(self) -> RTextBase:
65:             processed_text = RTextBase.from_any(processed_text)
74:             Create a context where all :class:`RTextMCDRTranslation` will use the given language to translate within
84:                             with RTextMCDRTranslation.language_context('en_us'):
85:                                     text: RTextMCDRTranslation = server.rtr('my_plugin.some_message')
102:    def to_json_object(self, **kwargs: Unpack[RTextBase.ToJsonKwargs]) -> Union[dict, list]:
118:    def copy(self) -> 'RTextMCDRTranslation':
119:            copied = RTextMCDRTranslation(self.translation_key, *self.args, **self.kwargs)
126:            def add_color(rt: RTextBase):
133:            def set_styles(rt: RTextBase):
140:            def set_click_event(rt: RTextBase):
147:            def set_hover_event(rt: RTextBase):
154:            def set_hover_text(rt: RTextBase):

docs\source\_locale\zh_CN\LC_MESSAGES\code_references\PluginServerInterface.po
123:"A neat command description. It can be a str or a :class:`RText "
124:"<mcdreforged.minecraft.rtext.text.RTextBase>` Also, it can be a dict maps"
127:"一个整洁的命令描述。它可以为一个 str 或者 :class:`RText "
128:"<mcdreforged.minecraft.rtext.text.RTextBase>`。除此之外它还可为一个将语言映射至描述信息的 dict"

mcdreforged\plugin\builtin\mcdr\mcdreforged_plugin.py
12:from mcdreforged.minecraft.rtext.click_event import RAction
13:from mcdreforged.minecraft.rtext.style import RColor
14:from mcdreforged.minecraft.rtext.text import RText
30:from mcdreforged.translation.translation_text import RTextMCDRTranslation
69:     def tr(self, key: str, *args, **kwargs) -> RTextMCDRTranslation:
130:                                    lst.append(RText(line).c(RAction.suggest_command, prefix.group()))

mcdreforged\plugin\meta\metadata.py
7:from mcdreforged.minecraft.rtext.text import RTextBase, RText
9:from mcdreforged.translation.translation_text import RTextMCDRTranslation
105:            if isinstance(self.name, RTextBase):
110:            if isinstance(description, RTextBase):
179:    def get_description_rtext(self) -> RTextBase:
181:            Return a translated plugin description in :class:`RText <mcdreforged.minecraft.rtext.text.RTextBase>`
188:                    return RText(self.description)
189:            return RTextMCDRTranslation.from_translation_dict(self.description)

mcdreforged\plugin\si\server_interface.py
26:from mcdreforged.translation.translation_text import RTextMCDRTranslation
185:            If args or kwargs contains :class:`RText <mcdreforged.minecraft.rtext.text.RTextBase>` element,
186:            then the result will be a :class:`RText <mcdreforged.minecraft.rtext.text.RTextBase>`,
200:    def rtr(self, translation_key: str, *args, **kwargs) -> RTextMCDRTranslation:
202:            Return a :class:`~mcdreforged.translation.translation_text.RTextMCDRTranslation` component,
207:            Of course, you can construct :class:`~mcdreforged.translation.translation_text.RTextMCDRTranslation` yourself instead of using this method if you want
215:            text = RTextMCDRTranslation(translation_key, *args, **kwargs)
463:            with RTextMCDRTranslation.language_context(self._mcdr_server.preference_manager.get_preferred_language(player)):
492:            with RTextMCDRTranslation.language_context(self._mcdr_server.preference_manager.get_console_preference().language):

docs\source\_locale\zh_CN\LC_MESSAGES\code_references\plugin.po
148:#: mcdreforged.plugin.meta.metadata.Metadata.get_description_rtext:1 of
150:"Return a translated plugin description in :class:`RText "
151:"<mcdreforged.minecraft.rtext.text.RTextBase>`"
153:"以 :class:`RText <mcdreforged.minecraft.rtext.text.RTextBase>` "

docs\source\_locale\zh_CN\LC_MESSAGES\code_references\command.po
117:" context with :meth:`RTextMCDRTranslation.language_context() "
118:"<mcdreforged.translation.translation_text.RTextMCDRTranslation.language_context>`"
121:":meth:`RTextMCDRTranslation.language_context() "
122:"<mcdreforged.translation.translation_text.RTextMCDRTranslation.language_context>`"
129:":class:`~mcdreforged.translation.translation_text.RTextMCDRTranslation`"
130:msgstr "类 :class:`~mcdreforged.translation.translation_text.RTextMCDRTranslation`"
179:"including RTexts"
180:msgstr "发送消息到命令源。消息可以是包括 RText 对象在内的任何内容"
368:"a :class:`~mcdreforged.minecraft.rtext.text.RTextBase`. Argument list: "
373:":class:`~mcdreforged.minecraft.rtext.text.RTextBase` "

mcdreforged\utils\misc_utils.py
10:     from mcdreforged.minecraft.rtext.text import RTextBase
11:     text_str = RTextBase.from_any(text).to_colored_text()

mcdreforged\plugin\installer\catalogue_access.py
7:from mcdreforged.minecraft.rtext.style import RColor
8:from mcdreforged.minecraft.rtext.text import RText
59:                             return RText('N/A', color=RColor.gray)
65:                                     return RText(result) + RText('...', color=RColor.gray)

mcdreforged\minecraft\rtext\style.py
7:from mcdreforged.minecraft.rtext._registry import RRegistry, NamedObject

mcdreforged\command\command_source.py
8:from mcdreforged.translation.translation_text import RTextMCDRTranslation
97:             with :meth:`RTextMCDRTranslation.language_context() <mcdreforged.translation.translation_text.RTextMCDRTranslation.language_context>`
101:                    Class :class:`~mcdreforged.translation.translation_text.RTextMCDRTranslation`
111:            with RTextMCDRTranslation.language_context(self.get_preference().language):
135:            Send a message to the command source. The message can be anything including RTexts

mcdreforged\minecraft\rtext\schema.py
6:class RTextJsonFormatItem:
11:class RTextJsonFormat(enum.Enum):
13:     Define the serialization format of :class:`RText <RTextBase>` components for different Minecraft versions
16:     V_1_7 = RTextJsonFormatItem('clickEvent', 'hoverEvent')
19:     V_1_21_5 = RTextJsonFormatItem('click_event', 'hover_event')
23:     def default(cls) -> 'RTextJsonFormat':
27:     def guess(cls, text_obj: dict) -> 'RTextJsonFormat':

docs\source\_locale\zh_CN\LC_MESSAGES\migrate\1.x_to_2.x.po
53:"You can no longer use :class:`RText "
54:"<mcdreforged.minecraft.rtext.text.RTextBase>` instance as the value of "
56:":class:`RText <mcdreforged.minecraft.rtext.text.RTextBase>` class will be"
59:"现在你不能使用 :class:`RText <mcdreforged.minecraft.rtext.text.RTextBase>` "
60:"实例作为插件元数据中键值对的值了。关于兼容性，以 :class:`RText "
61:"<mcdreforged.minecraft.rtext.text.RTextBase>` 类存在的 ``name`` 以及 "

docs\source\_locale\zh_CN\LC_MESSAGES\migrate\0.x_to_1.x.po
282:"If your plugin imports some of the mcdr utils, like ``RText`` or "
284:msgstr "如果你的插件需要导入一些 MCDR 内置模块，如 RText 或 Rcon，请查看模块的位置"
295:"Use ``from mcdreforged.api.rtext import *`` if you want to use all rtext "
297:msgstr "如需导入所有 RText 类，可使用 ``from mcdreforged.api.rtext import *``"

mcdreforged\plugin\si\plugin_server_interface.py
123:            :param message: A neat command description. It can be a str or a :class:`RText <mcdreforged.minecraft.rtext.text.RTextBase>`

mcdreforged\minecraft\rtext\hover_event.py
9:from mcdreforged.minecraft.rtext._registry import RRegistry, NamedObject
10:from mcdreforged.minecraft.rtext.schema import RTextJsonFormat
14:     from mcdreforged.minecraft.rtext.text import RTextBase
31:     show_text: ClassVar['RHoverAction[RHoverText]']
82:     def to_json_object(self, json_format: RTextJsonFormat) -> dict:
93:     def _to_json_object(self, json_format: RTextJsonFormat) -> dict:
98:     def from_json_object(cls, hover_event: dict, json_format: RTextJsonFormat) -> 'RHoverEvent':
114:    def _from_json_object(cls, click_event: dict, json_format: RTextJsonFormat) -> Self:
130:class RHoverText(RHoverEvent):
137:    text: 'RTextBase'
146:    def _to_json_object(self, json_format: RTextJsonFormat) -> dict:
148:            if json_format == RTextJsonFormat.V_1_7:
150:            elif json_format == RTextJsonFormat.V_1_21_5:
157:    def _from_json_object(cls, click_event: dict, json_format: RTextJsonFormat) -> Self:
158:            if json_format == RTextJsonFormat.V_1_7:
160:            elif json_format == RTextJsonFormat.V_1_21_5:
164:            from mcdreforged.minecraft.rtext.text import RTextBase
165:            return cls(text=RTextBase.from_json_object(text_obj))
186:    name: Optional[Union[str, 'RTextBase']] = None
197:    def _to_json_object(self, json_format: RTextJsonFormat) -> dict:
198:            from mcdreforged.minecraft.rtext.text import RTextBase
202:            elif isinstance(self.name, RTextBase):
207:            if json_format == RTextJsonFormat.V_1_7:
215:            elif json_format == RTextJsonFormat.V_1_21_5:
226:    def _from_json_object(cls, click_event: dict, json_format: RTextJsonFormat) -> Self:
227:            from mcdreforged.minecraft.rtext.text import RTextBase
229:            def deserialize_name(value: Any) -> Optional[Union[str, RTextBase]]:
233:                            return RTextBase.from_json_object(value)
245:            if json_format == RTextJsonFormat.V_1_7:
258:            elif json_format == RTextJsonFormat.V_1_21_5:
297:    def _to_json_object(self, json_format: RTextJsonFormat) -> dict:
298:            if json_format == RTextJsonFormat.V_1_7:
306:            elif json_format == RTextJsonFormat.V_1_21_5:
317:    def _from_json_object(cls, click_event: dict, json_format: RTextJsonFormat) -> Self:
318:            if json_format == RTextJsonFormat.V_1_7:
329:            elif json_format == RTextJsonFormat.V_1_21_5:
344:    register('show_text', RHoverText)

mcdreforged\plugin\builtin\mcdr\commands\sub_command.py
15:from mcdreforged.translation.translation_text import RTextMCDRTranslation
59:     def tr(self, key: str, *args, **kwargs) -> RTextMCDRTranslation:
97:     def can_see_rtext(source: CommandSource) -> bool:
111:                            source.reply(fut.result().to_rtext(self.mcdr_server, show_path=source.has_permission(PermissionLevel.PHYSICAL_SERVER_CONTROL_LEVEL)))

mcdreforged\minecraft\rtext\click_event.py
8:from mcdreforged.minecraft.rtext._registry import RRegistry, NamedObject
9:from mcdreforged.minecraft.rtext.schema import RTextJsonFormat
141:    def to_json_object(self, json_format: RTextJsonFormat) -> dict:
152:    def _to_json_object(self, json_format: RTextJsonFormat) -> dict:
157:    def from_json_object(cls, click_event: dict, json_format: RTextJsonFormat) -> 'RClickEvent':
173:    def _from_json_object(cls, click_event: dict, json_format: RTextJsonFormat) -> Self:
184:    .. seealso: :meth:`RTextBase.set_click_event(action, value) <mcdreforged.minecraft.rtext.text.RTextBase.set_click_event>`
190:    def _to_json_object(self, json_format: RTextJsonFormat) -> dict:
196:    def _from_json_object(cls, click_event: dict, json_format: RTextJsonFormat) -> Self:
201:    def _get_json_key(cls, json_format: RTextJsonFormat) -> str:
205:    def get_json_value(self, json_format: RTextJsonFormat) -> _JsonValueType:
232:    def _get_json_key(cls, json_format: RTextJsonFormat) -> str:
233:            return 'command' if json_format == RTextJsonFormat.V_1_21_5 else 'value'
236:    def get_json_value(self, json_format: RTextJsonFormat) -> str:
263:    def _get_json_key(cls, json_format: RTextJsonFormat) -> str:
264:            return 'command' if json_format == RTextJsonFormat.V_1_21_5 else 'value'
267:    def get_json_value(self, json_format: RTextJsonFormat) -> str:
294:    def _get_json_key(cls, json_format: RTextJsonFormat) -> str:
295:            return 'url' if json_format == RTextJsonFormat.V_1_21_5 else 'value'
298:    def get_json_value(self, json_format: RTextJsonFormat) -> str:
325:    def _get_json_key(cls, json_format: RTextJsonFormat) -> str:
326:            return 'path' if json_format == RTextJsonFormat.V_1_21_5 else 'value'
329:    def get_json_value(self, json_format: RTextJsonFormat) -> str:
356:    def _get_json_key(cls, json_format: RTextJsonFormat) -> str:
360:    def get_json_value(self, json_format: RTextJsonFormat) -> str:
393:    def _get_json_key(cls, json_format: RTextJsonFormat) -> str:
394:            return 'dialog' if json_format == RTextJsonFormat.V_1_21_5 else 'value'
397:    def get_json_value(self, json_format: RTextJsonFormat) -> Union[str, dict]:
398:            if json_format == RTextJsonFormat.V_1_7:
399:                    # This was introduced in mc1.21.5 and RTextJsonFormat.V_1_7 does not support this
412:#    str, in RTextJsonFormat.V_1_7
413:#    int, in RTextJsonFormat.V_1_21_5
433:    def _get_json_key(cls, json_format: RTextJsonFormat) -> str:
434:            return 'page' if json_format == RTextJsonFormat.V_1_21_5 else 'value'
437:    def get_json_value(self, json_format: RTextJsonFormat) -> Union[int, str]:
438:            return self.page if json_format == RTextJsonFormat.V_1_21_5 else str(self.page)
467:    def _to_json_object(self, json_format: RTextJsonFormat) -> dict:
468:            # introduced in mc1.21.6, so no need for handling RTextJsonFormat < V_1_21_5
476:    def _from_json_object(cls, click_event: dict, json_format: RTextJsonFormat) -> Self:
477:            # introduced in mc1.21.6, so no need for handling RTextJsonFormat < V_1_21_5

mcdreforged\plugin\builtin\mcdr\commands\preference_command.py
10:from mcdreforged.minecraft.rtext.click_event import RAction
11:from mcdreforged.minecraft.rtext.style import RColor, RStyle
12:from mcdreforged.minecraft.rtext.text import RTextList, RTextBase, RText
80:     def __detail_hint(self, text: RTextBase, pref_name: str) -> RTextBase:
83:                     h(self.tr('mcdr_command.preference.list.detail_hint', RText(pref_name, PREF_COLOR))).
91:                     value = getattr(pref, pref_name, RText('N/A', RColor.gray))
93:                             RTextList(RText('- ', RColor.gray), RText(pref_name, PREF_COLOR), RText(': ', RColor.gray), RText(value, VALUE_COLOR)),
106:                    text = RText(value, VALUE_COLOR).c(RAction.suggest_command, '{} preference {} set {}'.format(self.control_command_prefix, pref_name, value))
107:                    hover_text = RTextList(self.tr('mcdr_command.preference.item.set_suggestion_hint', RText(pref_name, PREF_COLOR), RText(value, VALUE_COLOR)))
109:                    extra_descriptions: List[RTextBase] = []
117:                            hover_text.append(RTextList('\n', RText.join(RText(', ', RColor.dark_gray), extra_descriptions)))
121:            source.reply(self.tr('mcdr_command.preference.item.name', self.__detail_hint(RText(pref_name, PREF_COLOR), pref_name)))
122:            source.reply(self.tr('mcdr_command.preference.item.value', RText(current_value, VALUE_COLOR)))
123:            source.reply(self.tr('mcdr_command.preference.item.suggestions', RText.join(', ', map(get_suggestion_text, entry.suggester()))))
134:            source.reply(self.tr('mcdr_command.preference.set.done', RText('language', RColor.yellow), RText(new_lang, RColor.gold)))

mcdreforged\translation\translation_manager.py
12:from mcdreforged.minecraft.rtext.text import RTextBase
73:             # Check if there's any rtext inside args and kwargs
74:             use_rtext = any([isinstance(e, RTextBase) for e in list(args) + list(kwargs.values())])
83:                             if use_rtext:
84:                                     translated_formatter = RTextBase.format(translated_formatter, *args, **kwargs)
94:                     return key if not use_rtext else RTextBase.from_any(key)

mcdreforged\command\command_manager.py
95:                             source.reply(error.to_rtext())

mcdreforged\plugin\builtin\mcdr\commands\pim_internal\texts.py
4:from mcdreforged.minecraft.rtext.click_event import RAction
5:from mcdreforged.minecraft.rtext.style import RColor, RStyle
6:from mcdreforged.minecraft.rtext.text import RTextBase, RText, RTextList
14:     def candidate(cls, plugin_id: str, version: Union[str, Version], /) -> RTextBase: ...
18:     def candidate(cls, candidate: PluginCandidate, /) -> RTextBase: ...
21:     def candidate(cls, *args) -> RTextBase:
28:                     return RTextList(
30:                             RText('@', RColor.gray),
37:     def cmd(cls, s: str, run: bool = False) -> RTextBase:
38:             return RText(s, color=RColor.gray).c(RAction.run_command if run else RAction.suggest_command, s)
41:     def diff_version(cls, base: Version, new: Version) -> RTextBase:
48:                     return RText(s2, RColor.gold)
50:                     return RText(s2[:i]) + RText(s2[i:], RColor.dark_aqua)
53:     def file_name(cls, name: str) -> RTextBase:
54:             return RText(name, color=RColor.dark_aqua)
57:     def file_path(cls, path: Union[str, Path]) -> RTextBase:
58:             return RText(path, color=RColor.dark_aqua).h(str(Path(path)))
61:     def number(cls, n: Union[int, float]) -> RTextBase:
62:             return RText(n, color=RColor.yellow)
65:     def plugin_id(cls, plugin_id: str) -> RTextBase:
66:             return RText(plugin_id, color=RColor.yellow)
69:     def url(cls, s: Any, url: str, *, color: RColor = RColor.blue, underlined: bool = True) -> RTextBase:
70:             text = RText(s, color=color).c(RAction.open_url, url)
76:     def version(cls, version: Union[str, Version]) -> RTextBase:
77:             return RText(version, color=RColor.gold)

mcdreforged\plugin\builtin\mcdr\commands\status_command.py
11:from mcdreforged.minecraft.rtext.click_event import RAction
12:from mcdreforged.minecraft.rtext.style import RColor, RStyle
13:from mcdreforged.minecraft.rtext.text import RText
27:             def bool_formatter(bl: bool) -> RText:
28:                     return RText(bl, RColor.green if bl else RColor.red)
37:                     h(RText(core_constant.GITHUB_URL, styles=RStyle.underlined, color=RColor.blue))
57:             source.reply(self.tr('mcdr_command.print_mcdr_status.extra.pid', process_pid if process_pid is not None else RText('N/A', RColor.gray)))

mcdreforged\plugin\builtin\mcdr\commands\help_command.py
8:from mcdreforged.minecraft.rtext.click_event import RAction
9:from mcdreforged.minecraft.rtext.style import RColor
10:from mcdreforged.minecraft.rtext.text import RText
46:                             source.reply(RText.format('{}: {}', RText(msg.prefix, color=RColor.gray).c(RAction.suggest_command, msg.prefix), msg.message))
52:                     prev_page = RText('<-', color=color[has_prev])
55:                     next_page = RText('->', color=color[has_next])
59:                     source.reply(RText.format('{} {} {}', prev_page, self.tr('mcdr_command.help_message.page_number', page), next_page))

mcdreforged\translation\functions.py
6:      from mcdreforged.translation.translation_text import RTextMCDRTranslation
16:     def __call__(self, key: str, *args, **kwargs) -> 'RTextMCDRTranslation':

mcdreforged\plugin\builtin\mcdr\commands\plugin_command.py
11:from mcdreforged.minecraft.rtext.click_event import RAction
12:from mcdreforged.minecraft.rtext.style import RColor, RStyle
13:from mcdreforged.minecraft.rtext.text import RTextList, RText
78:                     displayed_name = RText(meta.name)
79:                     if not self.can_see_rtext(source):
80:                             displayed_name += RText(' ({})'.format(plugin.get_identifier()), color=RColor.gray)
81:                     texts = RTextList(
82:                             RText('- ', RColor.gray),
87:                     if self.can_see_rtext(source) and not plugin.is_builtin():
90:                                     RText('[↻]', color=RColor.gray)
94:                                     RText('[↓]', color=RColor.gray)
98:                                     RText('[×]', color=RColor.gray)
104:            def get_file_name(fp) -> Tuple[str, RText]:
106:                    name_text = RText(name)
114:                    texts = RTextList(RText('- ', color=RColor.gray), file_name_text)
115:                    if self.can_see_rtext(source):
118:                                    RText('[✔]', color=RColor.gray)
127:                    texts = RTextList(RText('- ', color=RColor.gray), file_name_text)
128:                    if self.can_see_rtext(source):
131:                                    RText('[↑]', color=RColor.gray)
143:                    source.reply(RTextList(
144:                            RText(meta.name).set_color(RColor.yellow).set_styles(RStyle.bold).h(plugin),
146:                            RText('v{}'.format(meta.version), color=RColor.gray)
152:                            source.reply(self.tr('mcdr_command.plugin_info.link', RText(meta.link, color=RColor.blue, styles=RStyle.underlined).c(RAction.open_url, meta.link)))
154:                            source.reply(meta.get_description_rtext())

mcdreforged\plugin\builtin\mcdr\commands\permission_command.py
9:from mcdreforged.minecraft.rtext.click_event import RAction
10:from mcdreforged.minecraft.rtext.style import RColor
11:from mcdreforged.minecraft.rtext.text import RTextList, RText
101:                                    RTextList(RText('[', RColor.gray), RText(permission_level.name, RColor.yellow), RText(']', RColor.gray))
106:                                    texts = RTextList(RText('- ', RColor.gray), player)
107:                                    if self.can_see_rtext(source):
108:                                            texts += RTextList(
109:                                                    RText(' [✎]', color=RColor.gray)
112:                                                    RText(' [×]', color=RColor.gray)

mcdreforged\plugin\builtin\mcdr\commands\pim_internal\handler_browse.py
5:from mcdreforged.minecraft.rtext.click_event import RAction
6:from mcdreforged.minecraft.rtext.style import RColor
7:from mcdreforged.minecraft.rtext.text import RTextBase, RText, RTextList
31:             na = RText('N/A', color=RColor.gray)
42:                     def version_text(r: ReleaseData, anchor: bool) -> RTextBase:
43:                             text = RTextList(
46:                                     h(RTextBase.join('\n', [
53:                                             RText('*', color=RColor.blue).
70:                             line = RTextBase.join(', ', [versions[j] for j in range(i, min(i + 10, len(versions)))])
82:                             source.reply(RTextList(
84:                                     RText(': ', RColor.gray),

mcdreforged\plugin\plugin_registry.py
10:from mcdreforged.minecraft.rtext.text import RTextBase
12:from mcdreforged.translation.translation_text import RTextMCDRTranslation
29:             self.message: RTextBase
30:             if isinstance(message, RTextMCDRTranslation):
33:                     self.message = RTextMCDRTranslation.from_translation_dict(message)
35:                     self.message = RTextBase.from_any(message)

mcdreforged\api\rtext\__init__.py
1:# Link to mcdreforged.rtext
3:from mcdreforged.minecraft.rtext.click_event import RClickAction, RClickEvent, RAction, RClickSuggestCommand, RClickRunCommand, RClickOpenUrl, RClickOpenFile, RClickCopyToClipboard
4:from mcdreforged.minecraft.rtext.hover_event import RHoverAction, RHoverEvent, RHoverText, RHoverEntity, RHoverItem
5:from mcdreforged.minecraft.rtext.schema import RTextJsonFormat
6:from mcdreforged.minecraft.rtext.style import RColor, RStyle, RColorClassic, RColorRGB, RStyleClassic
7:from mcdreforged.minecraft.rtext.text import RTextTranslation, RTextList, RTextBase, RText
8:from mcdreforged.translation.translation_text import RTextMCDRTranslation
21:     'RHoverText', 'RHoverEntity', 'RHoverItem',
24:     'RTextBase', 'RText', 'RTextTranslation', 'RTextList',
25:     'RTextMCDRTranslation',
28:     'RTextJsonFormat',

mcdreforged\plugin\builtin\mcdr\commands\pim_internal\handler_install.py
17:from mcdreforged.minecraft.rtext.click_event import RAction
18:from mcdreforged.minecraft.rtext.style import RColor, RStyle
19:from mcdreforged.minecraft.rtext.text import RTextBase, RText
351:            source.reply(RTextBase.format(
366:                            RText(data.old_version) if data.old_version else RText('N/A', RColor.dark_gray),
376:                    source.reply(RTextBase.format(
385:                                    RText(req, RColor.blue).c(RAction.open_url, f'https://pypi.org/project/{req}/'),
393:            dry_run_suffix = self._tr('install.dry_run_suffix') if ctx.dry_run else RText('')
460:                                    hash_quoted=RText(f'({data.release.file_sha256})', color=RColor.gray),

mcdreforged\command\builder\exception.py
6:from mcdreforged.minecraft.rtext.text import RTextBase, RText, RColor
63:     def to_rtext(self) -> RTextBase:
64:             return RTextBase.format(
66:                     RTextBase.from_any(self.__message).copy().set_color(RColor.red),
67:                     RText(self.get_parsed_command(), RColor.dark_red),
68:                     RText(self.get_error_segment(), RColor.red),
69:                     RText('<--', RColor.dark_red)
145:    __NO_REASON = RText('Requirement not met')

mcdreforged\command\builder\nodes\basic.py
173:            :param failure_message_getter: An optional callable that accepts up to 2 arguments and returns a str or a :class:`~mcdreforged.minecraft.rtext.text.RTextBase`.

mcdreforged\plugin\builtin\mcdr\commands\pim_internal\handler_freeze.py
6:from mcdreforged.minecraft.rtext.style import RColor
7:from mcdreforged.minecraft.rtext.text import RTextBase, RText, RTextList
22:     def as_text(self) -> RTextBase:
25:                     RText('==', RColor.gray),
30:                             RText('@', RColor.gray),
31:                             RText(self.hash, RColor.dark_green),
33:             return RTextList(*args)

mcdreforged\plugin\builtin\mcdr\commands\pim_internal\handler_base.py
8:from mcdreforged.minecraft.rtext.click_event import RAction
9:from mcdreforged.minecraft.rtext.text import RTextBase
46:     def browse_cmd(self, plugin_id: str) -> RTextBase:

mcdreforged\api\all\__init__.py
21:from mcdreforged.api.rtext import *

mcdreforged\plugin\builtin\mcdr\commands\pim_internal\handler_check_update.py
8:from mcdreforged.minecraft.rtext.style import RColor, RStyle
9:from mcdreforged.minecraft.rtext.text import RTextBase, RText, RTextList
113:                    RTextBase.join(', ', [self._tr(k, Texts.number(n)) for n, k in kinds if n > 0])
123:                            texts = RTextList(
127:                                    RText(entry.current_version),
128:                                    RText(' -> ', RColor.gray),
150:                            source.reply(RTextList(
154:                                    RText(entry.current_version),
PS G:\GGames\Minecraft\aaaSERVERSaaa\aaa_from_git_aaa\github\MCDReforged> 
```