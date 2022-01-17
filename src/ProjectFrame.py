import wx
import wx.aui
from ObjectListView import ObjectListView, ColumnDefn


class ProjectFrame(wx.aui.AuiMDIChildFrame):
    def __init__(self, parent, projectData, databaseConnection):
        wx.aui.AuiMDIChildFrame.__init__(self, parent, wx.ID_ANY, style=wx.SUNKEN_BORDER, title=projectData[1])

        # Save data in memory
        self.projectData = projectData
        # Store database connection, there has to be a better way to do this
        self.databaseConnection = databaseConnection

        # Add a completion bar (that only loads on the opening of the program for now.)
        gauge = wx.Gauge(self, wx.ID_ANY, style=wx.GA_SMOOTH, range=0)

        # Create a scrollable, sortable, interactable list of all actions
        self.actionList = ObjectListView(self, wx.ID_ANY, style=wx.LC_REPORT | wx.BORDER_DEFAULT)
        self.actionList.SetColumns([
            ColumnDefn("Action", "center", -1, "Action", isSpaceFilling=True),
            ColumnDefn("Completed", "center", 130, "Completed"),
            ColumnDefn("Deadline", "center", 130, "Deadline")
        ])
        self.actionList.SetEmptyListMsg("Add an action to start tracking your project progress!")

        # Allow the completion to be changed by right-clicking (Not ideal, because how should an user know that.)
        self.actionList.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.change_completion)

        self.actions = databaseConnection.get_actions_of_project(str(projectData[0]))

        # While filling the actions the correct values for the completion gauge are set
        for current_action in self.actions:
            gauge.SetRange(gauge.GetRange() + 1)
            if current_action[3] == 1:
                gauge.SetValue(gauge.GetValue() + 1)
            self.actionList.AddObject(
                action(current_action[1], current_action[3], current_action[2], current_action[0]))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(gauge, 1, wx.EXPAND)
        sizer.Add(self.actionList, 100, wx.EXPAND)

        mb = parent.make_menu_bar()
        menu = wx.Menu()

        item = menu.Append(-1, "Add Action")
        self.Bind(wx.EVT_MENU, self.add_action, item)

        item = menu.Append(-1, "Delete Project")
        self.Bind(wx.EVT_MENU, self.delete_project, item)

        mb.Append(menu, "Project Menu")

        self.SetMenuBar(mb)
        self.SetSizer(sizer)
        wx.CallAfter(self.Layout)

    def delete_project(self, event):
        self.databaseConnection.remove_project(str(self.projectData[0]))
        self.Close()
        return

    def add_action(self, event):
        dlg = GetData(parent=self)
        dlg.ShowModal()
        if dlg.result_action_title:
            action_id = self.databaseConnection.add_action_to_project(dlg.result_action_title, dlg.result_deadline,
                                                                      str(self.projectData[0]))
            self.actionList.AddObject(action(dlg.result_action_title, 0, dlg.result_deadline, action_id))
        dlg.Destroy()
        return

    def change_completion(self, event):
        selected_action = self.actionList.GetSelectedObject()
        selected_action.switch_completion(self.databaseConnection)
        self.actionList.RefreshObject(selected_action)


class action:
    def __init__(self, Action, Completed, Deadline, id):
        self.id = id
        self.Action = Action
        if Completed == 1:
            self.Completed = True
        else:
            self.Completed = False
        self.Deadline = Deadline

    def switch_completion(self, databaseConnection):
        if self.Completed is True:
            self.Completed = False
        else:
            self.Completed = True
        databaseConnection.change_completion(self.Completed, self.id)


class GetData(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Add new action", size=(650, 220))
        self.result_action_title = None
        self.result_deadline = None

        self.panel = wx.Panel(self, wx.ID_ANY)
        self.lbltitle = wx.StaticText(self.panel, label="Action title", pos=(20, 20))
        self.title = wx.TextCtrl(self.panel, value="", pos=(110, 20), size=(500, -1))
        self.lbldeadline = wx.StaticText(self.panel, label="Deadline", pos=(20, 60))
        self.deadline = wx.TextCtrl(self.panel, value="", pos=(110, 60), size=(500, -1))

        self.saveButton = wx.Button(self.panel, label="Save", pos=(110, 160))
        self.closeButton = wx.Button(self.panel, label="Cancel", pos=(210, 160))

        self.saveButton.Bind(wx.EVT_BUTTON, self.SaveConnString)
        self.closeButton.Bind(wx.EVT_BUTTON, self.OnQuit)

        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        self.Show()

    def OnQuit(self, event):
        self.Destroy()

    def SaveConnString(self, event):
        self.result_action_title = self.title.GetValue()
        self.result_deadline = self.deadline.GetValue()
        self.Destroy()
