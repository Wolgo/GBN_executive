import wx
import wx.aui

from DatabaseHandler import DatabaseHandler
from ProjectFrame import ProjectFrame


class ExecutiveMainFrame(wx.aui.AuiMDIParentFrame):
    def __init__(self):
        wx.aui.AuiMDIParentFrame.__init__(self, None, wx.ID_ANY,
                                          title='GBN Executive',
                                          size=(900, 400),
                                          style=wx.DEFAULT_FRAME_STYLE)

        self.SetMenuBar(self.make_menu_bar())

        # Create a tab for each project
        self.projects = databaseConnection.get_projects()
        for project in self.projects:
            ProjectFrame(self, project, databaseConnection)

    def make_menu_bar(self):
        mb = wx.MenuBar()
        menu = wx.Menu()

        item = menu.Append(-1, "New Project")
        self.Bind(wx.EVT_MENU, self.create_new_project, item)

        item = menu.Append(-1, "Close Executive")
        self.Bind(wx.EVT_MENU, self.OnDoClose, item)

        mb.Append(menu, "&File")
        return mb

    def create_new_project(self, evt):
        # ! currently this does not prevent duplicate project names and some wierd behaviour because of it

        # Pop-up dialog for text input
        dlg = wx.TextEntryDialog(frame, 'Title of new project:', 'New Project')
        dlg.SetValue("Default")

        if dlg.ShowModal() == wx.ID_OK:
            try:
                databaseConnection.add_project(dlg.GetValue())
                # First add the project and then retrieve it to have access to the project id
                project = databaseConnection.get_project_by_title(dlg.GetValue())
                databaseConnection.commit()
                for project in project:
                    child = ProjectFrame(self, project, databaseConnection)
                    child.Show()
            except Exception as data:
                print(data)

    # Save Changes when the menu button is used to exit
    def OnDoClose(self, evt):
        databaseConnection.commit()
        self.Close()


if __name__ == '__main__':
    # Create Database connection
    global databaseConnection
    databaseConnection = DatabaseHandler()

    # Prepare and launch gui
    app = wx.App()
    frame = ExecutiveMainFrame()
    frame.Show()
    app.MainLoop()
