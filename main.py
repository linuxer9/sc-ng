from gi.repository import Gtk, Gdk, GdkPixbuf
import PK

class SC():
	def __init__(self):
		
		self.init_Gui()
		#TODO: Loading window
		self.client = PK.PKClient()
		self.packages = self.client.GetPackages()
		self.apply_css()
		self.window.show_all()


	def init_Gui(self):
		#Glade file(s)
		Gui = Gtk.Builder()
		Gui.add_from_file("ui.glade")
		#window stuff
		self.window = Gui.get_object("window1")
		self.window.connect("delete-event", Gtk.main_quit)
		#icons 
		self.icon_store = Gtk.IconTheme()
		self.icon_store.prepend_search_path("/usr/share/app-install/icons")
		self.content = Gui.get_object("content")
		self.header = Gui.get_object("header")
		Gui.connect_signals({"group_clicked":self.group_clicked})
		#TODO: welcome screen
		

	def add_package(self, id, title, desc, icon = None):
		
		#Disposal GtkBuilder 
		dB= Gtk.Builder()
		dB.add_from_file("list_widget.glade")
		#main widget		
		pack = dB.get_object("pack")
		pack.connect("clicked", self.pack_clicked, id)
		#package title
		pack_title = dB.get_object("app_title")
		pack_title.set_text(title)
		#package summary
		pack_desc= dB.get_object("app_desc")
		pack_desc.set_text(desc)
		#package icon
		if icon:
			pack_icon = dB.get_object("app_icon")
			try:
				pack_icon.set_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_scale(icon,48,48,True))
			except: pass
		# then, finish it
		self.packages_list.add(pack)

	def apply_css(self):
		cssProvider = Gtk.CssProvider()
		cssProvider.load_from_path('styles.css')
		screen = Gdk.Screen.get_default()
		styleContext = Gtk.StyleContext()
		styleContext.add_provider_for_screen(screen, cssProvider,
		Gtk.STYLE_PROVIDER_PRIORITY_USER)

	def group_init(self, title,icon = None):
		#TODO: store it in navigation
		if len(self.header.get_children() ) >0:
			for widget in self.header.get_children():
				self.header.remove(widget)

		if len(self.content.get_children() ) >0:
			for widget in self.content.get_children():
				self.content.remove(widget)
		#Disposal GtkBuilder 
		dB= Gtk.Builder()
		dB.add_from_file("category_view.glade")
		category_header = dB.get_object("category_header")
		category_title = dB.get_object("category_title")
		category_title.set_text(title)
		if icon:
			category_icon = dB.get_object("category_icon")
			category_icon.set_from_file("categories/icons/"+icon)
		self.header.add(category_header)
		packages_list_container = dB.get_object("packages_list")
		self.packages_list = dB.get_object("packages_list_content")
		self.content.add(packages_list_container)
		

		
	def group_clicked(self, widget):
		#TODO: show loading picture
		group_file = open("categories/" + widget.get_name(),'r')
		group_data = group_file.read().split()
		group_file.close()
		group_label = widget.get_label()
		self.group_init(group_label, widget.get_name().split('.list')[0]+'.svg')
		packages_list = [pack for pack in self.packages if pack[0] in group_data]
		for pack in packages_list:
			self.add_package(pack[1], pack[0].title(),pack[2], self.get_icon(pack[0]))
			
	def pack_clicked(self, widget, id):
		print(id+" pressed")

	def get_icon(self, package):
		icon = self.icon_store.lookup_icon(package,48,0)
		if icon is not None:
			return icon.get_filename() 
		else:
			return "icons/default.png"
SC()		
Gtk.main()
