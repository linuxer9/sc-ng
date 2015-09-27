from gi.repository import Gtk, Gdk, GdkPixbuf
import PK

class SC():
	def __init__(self):
		
		self.init_Gui()
		#TODO: Loading window

		self.apply_css()
		self.window.show_all()
		self.after_finish = None
		self.client = PK.PKClient(self.finished)		
		self.load_database()
		


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
		self.groups_list = Gui.get_object("groups_list")
		Gui.connect_signals({"group_clicked":self.group_clicked})
		self.loading_icon = Gtk.Image()
		spin_animation = GdkPixbuf.PixbufAnimation.new_from_file("icons/spinner.gif")
		self.loading_icon.set_from_animation(spin_animation)
		#TODO: welcome screen
		
		

	def load_database(self):
		
		self.content.add(self.loading_icon)
		self.loading_icon.show()

		for widget in self.groups_list:
			widget.set_sensitive(False)
		def after_finish():
			for widget in self.groups_list:
				widget.set_sensitive(True)
			self.content.remove(self.loading_icon)
			self.after_finish = None
		self.after_finish = after_finish
		self.packages = self.client.GetPackages()

	def finished(self):
		if self.after_finish:
			self.after_finish()

	def add_package(self, id, title, desc, status, icon = None):
		
		#Disposal GtkBuilder 
		dB= Gtk.Builder()
		dB.add_from_file("list_widget.glade")
		#main widget		
		pack = dB.get_object("pack")
		pack.connect("clicked", self.pack_clicked, [id,status, desc])
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

	def group_init(self, button, title,icon = None):
		#TODO: store it in navigation
		self.content_clean()
		for child_widget in self.groups_list.get_children():
			if child_widget != button:	
				child_widget.set_active(False)
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
		self.group_init(widget, group_label, widget.get_name().split('.list')[0]+'.svg')
		packages_list = [pack for pack in self.packages if pack[0] in group_data]
		for pack in packages_list:
			self.add_package(pack[1], pack[0].title(),pack[2], pack[3], self.get_icon(pack[0], 48))
			
	def pack_clicked(self, widget, info):
		id = info[0]
		status = info[1]
		summary = info[2]
		details = self.client.GetDetails([id])

		self.content_clean()
		#Disposal GtkBuilder 
		dB= Gtk.Builder()
		dB.add_from_file("package_view.glade")
		package_header = dB.get_object("package_header")
		package_title = dB.get_object("package_title")
		package_title.set_text(id.split(';')[0])
		package_summary = dB.get_object("package_summary")
		package_summary.set_text(summary)
		package_icon = dB.get_object("package_icon")
		icon = self.get_icon(id.split(';')[0], 64)
		try:
			package_icon.set_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_scale(icon,64,64,True))
		except: pass
		action_button = dB.get_object("action_button")
		if status == "available":
			action_button.set_name("install_button")
			action_button.set_label("Install")
		if status == "installed":
			action_button.set_name("remove_button")
			action_button.set_label("Remove")
		self.header.add(package_header)

		package_details = dB.get_object("package_details")
		package_desc = dB.get_object("package_desc")
		package_desc.set_text(str(details[3]))
		self.content.add(package_details)
		
	def content_clean(self):
		if len(self.header.get_children() ) >0:
			for widget in self.header.get_children():
				self.header.remove(widget)

		if len(self.content.get_children() ) >0:
			for widget in self.content.get_children():
				self.content.remove(widget)


	def get_icon(self, package, size):
		icon = self.icon_store.lookup_icon(package,size,0)
		if icon is not None:
			return icon.get_filename() 
		else:
			return "icons/default.png"
SC()		
Gtk.main()
