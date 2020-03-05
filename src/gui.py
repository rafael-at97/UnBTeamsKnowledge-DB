# coding: utf-8

import wx
import wx.lib.mixins.listctrl as listmix

class SimpleDialog(wx.Dialog):
    def __init__(self, parent, title, entries_labels=[]):
        wx.Dialog.__init__(self, parent, title=title, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)

        #self.Bind(wx.EVT_CLOSE, self.OnClose)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_panel = wx.Panel(self)
        panel_sizer = wx.BoxSizer(wx.VERTICAL)
        main_panel.SetSizer(panel_sizer)

        self.entries_sizer = self.MakeEntries(main_panel, entries_labels)
        buttons = self.MakeButtons(main_panel)

        panel_sizer.Add(self.entries_sizer, flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, border=5)
        panel_sizer.Add(wx.StaticLine(main_panel), 0, wx.ALL|wx.EXPAND, border=5)
        panel_sizer.Add(buttons, flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, border=5)

        main_sizer.Add(main_panel)
        self.SetSizer(main_sizer)

        panel_sizer.Fit(self)

    def MakeEntries(self, parent, entries_labels):
        entries_sizer = wx.FlexGridSizer(2, 5, 5)

        entry_msg = []
        self.entry = []
        for i in range(len(entries_labels)):
            entry_msg.append(wx.StaticText(parent, label=entries_labels[i]))
            self.entry.append(wx.TextCtrl(parent))    

        for i in range(len(entries_labels)):
            entries_sizer.Add(entry_msg[i], 1, flag=wx.ALIGN_RIGHT)
            entries_sizer.Add(self.entry[i], 1, flag=wx.ALIGN_LEFT)

        entries_sizer.AddGrowableCol(0)
        entries_sizer.AddGrowableCol(1)

        return entries_sizer

    def MakeButtons(self, parent):
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.ok_button = wx.Button(parent, wx.ID_OK, 'Ok')
        self.cancel_button = wx.Button(parent, wx.ID_CANCEL, 'Cancelar')

        self.ok_button.SetDefault()

        sizer.Add(self.ok_button, proportion=1)
        sizer.AddStretchSpacer()
        sizer.Add(self.cancel_button, proportion=1)

        return sizer  

class CustomList(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES, size=(-1, -1), fields=[]):

        wx.ListCtrl.__init__(self, parent, style=style, size=size)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

        for i in range(len(fields)):
            self.InsertColumn(i, fields[i], width=-1)

        self.setResizeColumn(0)

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        # Start based on display size
        display_size = wx.DisplaySize()
        # Make it known to the whole object
        self.frame_size = (display_size[0]*0.50,display_size[1]*0.60)

        wx.Frame.__init__(self, parent, title=title, size=self.frame_size)

        # Menu related
        self.MakeMenu()

        # Panel initialization
        main_panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_panel.SetSizer(main_sizer)

        projects_box = self.CreateProjectsBox(main_panel)
        filter_box = self.CreateFilterBox(main_panel)

        # Adds the childs to the super boxsizer
        main_sizer.Add(projects_box, proportion=1, flag=wx.EXPAND|wx.RIGHT|wx.LEFT|wx.TOP, border=7)
        main_sizer.Add(filter_box, proportion=1, flag=wx.EXPAND|wx.RIGHT|wx.LEFT|wx.TOP, border=7)

        self.Show(True)

    def MakeMenu(self):
        main_menubar = wx.MenuBar()

        add_menu = wx.Menu()
        equipe_item = wx.MenuItem(add_menu, id=wx.ID_ANY, text="Equipe")
        int_item = wx.MenuItem(add_menu, id=wx.ID_ANY, text="Integrante")
        comp_item = wx.MenuItem(add_menu, id=wx.ID_ANY, text="Competição")
        proj_item = wx.MenuItem(add_menu, id=wx.ID_ANY, text="Projeto")
        area_item = wx.MenuItem(add_menu, id=wx.ID_ANY, text="Área de conhecimento")
        add_menu.AppendItem(equipe_item)
        add_menu.AppendItem(int_item)
        add_menu.AppendItem(comp_item)
        add_menu.AppendItem(proj_item)
        add_menu.AppendItem(area_item)        

        main_menubar.Append(add_menu, '&Adicionar')

        self.Bind(wx.EVT_MENU, self.AddTeam, equipe_item)
        #self.Bind(wx.EVT_MENU, self.ManageAdmins, config_admin)
        self.Bind(wx.EVT_MENU, self.AddArea, area_item)

        self.SetMenuBar(main_menubar)

    def CreateProjectsBox(self, parent):
        projects_box_sizer = wx.StaticBoxSizer(wx.VERTICAL, parent, "Projetos")

        # ListCtrl to show data about projects
        self.projects_list = self.CreateBoxList(parent, ["Nome"], button_name="Sobre")

        # Add widgets to projects_box
        projects_box_sizer.Add(self.projects_list, proportion=1, flag=wx.EXPAND|wx.RIGHT|wx.LEFT, border=5)

        return projects_box_sizer        

    def CreateFilterBox(self, parent):
        filter_box_sizer = wx.StaticBoxSizer(wx.HORIZONTAL, parent, "Pesquisa")

        # ListCtrls
        self.search_area_list = self.CreateBoxList(parent, ["Área"])
        self.search_team_list = self.CreateBoxList(parent, ["Equipe"])

        # Add widgets to projects_box
        filter_box_sizer.Add(self.search_area_list, proportion=1, flag=wx.EXPAND|wx.RIGHT|wx.LEFT, border=5)
        filter_box_sizer.Add(self.search_team_list, proportion=1, flag=wx.EXPAND|wx.RIGHT|wx.LEFT, border=5)

        return filter_box_sizer

    def CreateBoxList(self, parent, fields, button_name="Pesquisar"):
        box_sizer = wx.BoxSizer(wx.VERTICAL)

        # ListCtrl to show data about projects
        my_list = CustomList(parent, fields=fields)

        # Button to show info
        search_button = wx.Button(parent, size=(self.frame_size[0]*0.33, self.frame_size[1]*0.06), label=button_name)

        # Bind button
        #remove_user.Bind(wx.EVT_BUTTON, self.RemoveUser)

        # Add widgets to projects_box
        box_sizer.Add(my_list, proportion=1, flag=wx.EXPAND|wx.RIGHT|wx.LEFT, border=5)
        box_sizer.Add(search_button, flag=wx.ALIGN_CENTER|wx.TOP, border=2)

        return box_sizer

    def AddTeam(self, event):
        # Open another window to add team
        dialog = SimpleDialog(self, title="Adicionar Equipe", entries_labels=["Nome: ", "Curso: "])
        dialog.ShowModal()

        dialog.Destroy()

        event.Skip()        

    def AddArea(self, event):
        # Open another window to add team
        dialog = SimpleDialog(self, title="Adicionar Área de Conhecimento", entries_labels=["Nome: ", "Macro-Área: "])
        dialog.ShowModal()

        dialog.Destroy()

        event.Skip()        

def main():
    main_app = wx.App(False)

    gui = MainWindow(None, "Projeto BD")

    main_app.MainLoop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program closing abruptly!")