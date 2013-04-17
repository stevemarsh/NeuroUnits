import  wx

import glob
import datetime

import numpy

import wx
import wx.gizmos as gizmos



import neurounits
import neurounits.ast as ast
srcs = sorted( glob.glob("/home/michael/hw/NeuroUnits/src/test_data/l4-9ml/std/*.9ml"))
srcs = sorted( glob.glob("/home/michael/hw/NeuroUnits/src/test_data/l4-9ml/examples/*.9ml"))
lib_mgr = neurounits.NeuroUnitParser.Parse9MLFiles(srcs)












class RunDialog(wx.Dialog):
    
    def __init__(self, *args, **kw):
        assert 'component' in kw
        self.component = kw['component']
        del kw['component']
        
        super(RunDialog, self).__init__(*args, **kw) 
        
        
        self.InitUI()
        self.SetSize((250, 200))
        self.SetTitle("Run component")
        
        
    def InitUI(self):

        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        sb = wx.StaticBox(pnl, label='Colors')
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)        
        sbs.Add(wx.RadioButton(pnl, label='256 Colors', style=wx.RB_GROUP))
        sbs.Add(wx.RadioButton(pnl, label='16 Colors'))
        sbs.Add(wx.RadioButton(pnl, label='2 Colors'))
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)        
        hbox1.Add(wx.RadioButton(pnl, label='Custom'))
        hbox1.Add(wx.TextCtrl(pnl), flag=wx.LEFT, border=5)
        sbs.Add(hbox1)
        
        pnl.SetSizer(sbs)
       
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        runButton = wx.Button(self, label='Run!')
        closeButton = wx.Button(self, label='Close')
        hbox2.Add(runButton)
        hbox2.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(pnl, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox2, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.SetSizer(vbox)
        
        runButton.Bind(wx.EVT_BUTTON, self.DoRun)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)
        
    
        
    def OnClose(self, e):
        self.Destroy()


    def DoRun(self, evt):
        print 'RUNNNIGN!', self.component 
        res = neurounits.nineml.simulate_component(self.component, numpy.arange(0,1.1,0.0001) )
        neurounits.nineml.auto_plot(res)
        import pylab
        pylab.show()









class TabPanel1(wx.Panel):

    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        self.tree = wx.TreeCtrl(self, 1, wx.DefaultPosition, (-1,-1), wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS|wx.EXPAND)

        # Setup the image lists:
        self.isz=(16,16)
        self.il = wx.ImageList(16,16)
        self.im_fldridx = self.il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, self.isz))
        self.im_fldropenidx = self.il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, self.isz))
        self.tree.SetImageList(self.il)
        self.tree.AssignImageList(self.il)


        
        
        self.build_tree()
        
        self.tree.Bind(wx.EVT_CONTEXT_MENU,self.showPopupMenu)


        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.tree, 1, wx.EXPAND)
        self.SetSizer(vbox)
        self.Centre()
        
    def build_tree(self):
        root = self.tree.AddRoot('')
        os = self.tree.AppendItem(root, 'Operating Systems')
        pl = self.tree.AppendItem(root, 'Programming Languages')
        tk = self.tree.AppendItem(root, 'Toolkits')
        self.tree.AppendItem(os, 'Linux')
        
        
    def showPopupMenu(self,evt):
        position = self.ScreenToClient(wx.GetMousePosition())

        
        obj = self.tree.GetPyData(self.tree.GetSelection() )
        print obj
        
        menu = wx.Menu()
        
        # Actions for 9ML component:
        if isinstance(obj, ast.NineMLComponent):
            run_id = wx.NewId()
            other_id = wx.NewId()
            menu.Append(run_id, 'Run:' + obj.name)
            menu.Append(other_id,'Item 2')
            
            # The handler:
            def my_run(evt):
                # Run the component?:
                if evt.GetId() == run_id:
                    chgdep = RunDialog(None, component=obj,) # title='Change Color Depth')
                    chgdep.ShowModal()
                    chgdep.Destroy()
                    
                elif evt.GetId() == other_id:
                    print 'Somehting else!', obj
            self.Bind(wx.EVT_MENU, my_run)
        
        
        self.PopupMenu(menu, self.ScreenToClient(wx.GetMousePosition()))


class TreeByModule(TabPanel1):
    
    def build_tree(self):
        root = self.tree.AddRoot('')
        modules = lib_mgr.get_modules()
        for m in modules:
            br = self.tree.AppendItem(root, 'Module: %s' % m)
            sub_comps = lib_mgr.get_all_in_module(m)
            for sc in sub_comps:
                itm = self.tree.AppendItem(br, 'Obj:  %s %s' % (type(sc).__name__.split('.')[-1], sc.name) )
                self.tree.SetPyData(itm, sc)
            
                self.tree.SetItemImage(itm, self.im_fldridx, wx.TreeItemIcon_Normal)
                self.tree.SetItemImage(itm, self.im_fldropenidx, wx.TreeItemIcon_Expanded)
        self.tree.ExpandAll()
        
        
        
class TreeByType(TabPanel1):
    def build_tree(self):
        #raise NotImplementedError()
        root = self.tree.AddRoot('')
        os = self.tree.AppendItem(root, 'Operating Systems')
        pl = self.tree.AppendItem(root, 'Programming Languages')
        tk = self.tree.AppendItem(root, 'Toolkits')
        self.tree.AppendItem(os, 'Linux')
        
class TreeByFile(TabPanel1):
    def build_tree(self):
        #raise NotImplementedError()
        root = self.tree.AddRoot('')
        os = self.tree.AppendItem(root, 'Operating Systems')
        pl = self.tree.AppendItem(root, 'Programming Languages')
        tk = self.tree.AppendItem(root, 'Toolkits')
        self.tree.AppendItem(os, 'Linux')






class LHSPanel(wx.Choicebook):
    
    def __init__(self, parent, **kwargs):
        global lib_mgr
        
        #wx.Panel.__init__(self, parent, **kwargs)
        wx.Choicebook.__init__(self, parent, wx.ID_ANY)
        
        tab1 = TreeByModule(self)
        tab1.SetBackgroundColour("Gray")
        self.AddPage(tab1, "By module")
        
        tab2 = TreeByType(self)
        tab2.SetBackgroundColour("Gray")
        self.AddPage(tab2, "By type")
        
        tab3 = TreeByFile(self)
        tab3.SetBackgroundColour("Gray")
        self.AddPage(tab3, "By file")
        
        self.tabs = [tab1, tab2, tab3]



class RHSPanelLibrary(wx.Panel):
    def __init__(self, parent, **kwargs):
        wx.Panel.__init__(self, parent, **kwargs)

        vbox = wx.BoxSizer(wx.VERTICAL)
        self.objlabel = wx.StaticText(self, -1, 'Library:')
        vbox.Add(self.objlabel, 1, wx.EXPAND)

        self.SetSizer(vbox)
        self.Centre()
        self.Layout()
        
    def set_obj(self, component):
        self.objlabel.SetLabel('Details for component:' + component.name) 


class RHSPanelInterface(wx.Panel):
    def __init__(self, parent, **kwargs):
        wx.Panel.__init__(self, parent, **kwargs)


        vbox = wx.BoxSizer(wx.VERTICAL)
        
        
        self.objlabel = wx.StaticText(self, -1, 'Interaface:')
        self.SetSizer(vbox)
        self.Centre()
        self.Layout()
    
    def set_obj(self, component):
        self.objlabel.SetLabel('Details for component:' + component.name) 
        
class RHSPanelModule(wx.Panel):
    def __init__(self, parent, **kwargs):
        wx.Panel.__init__(self, parent, **kwargs)


        vbox = wx.BoxSizer(wx.VERTICAL)
        
        
        self.objlabel = wx.StaticText(self, -1, 'Module:')
        self.SetSizer(vbox)
        self.Centre()
        self.Layout()
        
    
    def set_obj(self, component):
        self.objlabel.SetLabel('Details for component:' + component.name) 


class RHSPanelComponent(wx.Panel):
    def __init__(self, parent, **kwargs):
        wx.Panel.__init__(self, parent, **kwargs)


        vbox = wx.BoxSizer(wx.VERTICAL)
        
        
        self.objlabel = wx.StaticText(self, -1, 'Object:')
        
        self.list_ctrl_terminals = wx.ListCtrl(self, size=(-1,100), style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        self.list_ctrl_terminals.InsertColumn(0, 'Subject')
        self.list_ctrl_terminals.InsertColumn(1, 'Type')
        self.list_ctrl_terminals.InsertColumn(2, 'Dimension', width=125)
        
        
        self.list_ctrl_interfaces = wx.ListCtrl(self, size=(-1,100), style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        self.list_ctrl_interfaces.InsertColumn(0, 'Connector Name')
        self.list_ctrl_interfaces.InsertColumn(1, 'InterfaceType')
        self.list_ctrl_interfaces.InsertColumn(2, 'Direction', width=125)
        
        vbox.Add(self.objlabel, 1, wx.EXPAND)
        vbox.Add(self.list_ctrl_terminals, 3, wx.EXPAND)
        vbox.Add(self.list_ctrl_interfaces, 3, wx.EXPAND)

        self.SetSizer(vbox)
        self.Centre()
        self.Layout()


    def set_obj(self, component):
        
        self.list_ctrl_terminals.DeleteAllItems()
        self.list_ctrl_interfaces.DeleteAllItems()
        
        if component is None:
            print 'No component found'
            return 

        # Set the name:
        self.objlabel.SetLabel('Details for component:' + component.name) 


        for index, obj in enumerate( component.all_terminal_objs() ):
       
            self.list_ctrl_terminals.InsertStringItem(index, obj.symbol)
            self.list_ctrl_terminals.SetStringItem(index, 1, type(obj).__name__.split('.')[-1] )
            self.list_ctrl_terminals.SetStringItem(index, 2, str(obj.get_dimension()) )
            

        for index, obj in enumerate( component._compound_ports_connectors ):       
            self.list_ctrl_interfaces.InsertStringItem(index, obj.symbol)
            self.list_ctrl_interfaces.SetStringItem(index, 1, type(obj).__name__.split('.')[-1] )
            self.list_ctrl_interfaces.SetStringItem(index, 2, '' )
            
            

 
import images
import images
import wx
#import panelOne, panelTwo, panelThree

def getNextImageID(count):
    imID = 0
    while True:
        yield imID
        imID += 1
        if imID == count:
            imID = 0

class RHSToolbookDemo(wx.Toolbook):
    """
    Toolbook class
    """

    #----------------------------------------------------------------------
    def __init__(self, parent, style):
        """Constructor"""
        wx.Toolbook.__init__(self, parent, wx.ID_ANY, )
        
        # make an image list using the LBXX images
        il = wx.ImageList(24, 24)
        for x in range(3):
            obj = getattr(images, 'LB%02d' % (x+1))
            bmp = obj.GetBitmap()
            il.Add(bmp)
        self.AssignImageList(il)
        imageIdGenerator = getNextImageID(il.GetImageCount())
        
        
        page_types = (
            (neurounits.ast.NineMLComponent, RHSPanelComponent, "Component"),
            (neurounits.ast.CompoundPortDef, RHSPanelInterface, "Interface"),
            (neurounits.ast.Library, RHSPanelInterface, "Library"),
            (None, RHSPanelModule, "Module"),
        )
        
        self.page_map = {}
        

        for index, (objtype, pagetype, label) in enumerate(page_types):
            page = pagetype(self)
            self.page_map[objtype] = index, page
            self.AddPage(page, label, imageId=imageIdGenerator.next())
           
 
 
 
 
 
 
 
 
 
 
        
            
            

class MyFrame(wx.Frame):
    def __init__(self, parent, **kwargs):
        wx.Frame.__init__(self, parent, **kwargs)
        self.splitter = wx.SplitterWindow(self)
        
        self.lhs = LHSPanel(self.splitter, style=wx.BORDER_SUNKEN)
        self.lhs.SetBackgroundColour("orange")
    
        self.rhs = RHSToolbookDemo(self.splitter, style=wx.BORDER_SUNKEN) 
        
        self.splitter.SplitVertically(self.lhs, self.rhs)

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.change_obj)
        self.Centre()

    def change_obj(self, evt,):
        print 'Section Changed (parent)'
        
        tree = self.lhs.tabs[self.lhs.GetSelection()].tree
        obj = tree.GetPyData(tree.GetSelection() )
        
        
        obj_type = type(obj)
        
        if obj_type in self.rhs.page_map:
            page_index, page = self.rhs.page_map[obj_type]
            self.rhs.ChangeSelection(page_index)
            page.set_obj(obj)
        else:
            page_index, page = self.rhs.page_map[None]
            self.rhs.ChangeSelection(page_index)
            page.set_obj(obj)


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = MyFrame(None,  size=(1000,480))
    frame.Show()
    app.MainLoop()
