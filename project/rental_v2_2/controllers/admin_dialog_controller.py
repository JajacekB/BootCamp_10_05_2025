from PySide6.QtCore import QObject

from gui.windows.admin_dialog import AdminDialog

from gui.widgets.register_user_view import RegisterUserView
from controllers.register_user_controller import RegisterUserController

from gui.widgets.delete_users_view import DeleteUsersWidget
from repositories.delete_users_service import DeleteUsersService
from controllers.delete_users_controller import DeleteUsersController

from gui.widgets.get_users_view import GetUsersWidget
from repositories.get_users_service import GetUsersService
from controllers.get_users_controller import GetUsersController

from gui.widgets.get_vehicle_view import GetVehicleView
from repositories.get_vehicle_service import GetVehicleService
from controllers.get_vehicle_controller import GetVehicleController

from repositories.repair_service import RepairService
from gui.widgets.repair_view import RepairVehicleView
from controllers.repair_controller import RepairController

from gui.widgets.return_vehicle_view import ReturnVehicleView
from repositories.return_vehicle_service import ReturnVehicleService
from controllers.return_vehicle_controller import ReturnVehicleController

from gui.widgets.delete_vehicle_view import DeleteVehicleView
from controllers.delete_vehicle_controller import DeleteVehicleController

from gui.widgets.promo_banner_view import PromoBannerView
from controllers.promo_banner_controller import PromoBannerController

from gui.widgets.update_user_view import UpdateUserView
from controllers.update_user_controller import UpdateUserController

from gui.widgets.add_vehicle_view import AddVehicleView
from controllers.add_vehicle_controller import AddVehicleController

from gui.widgets.overdue_rental_view import OverdueRentalView
from controllers.overdue_rental_controller import OverdueRentalController

from gui.windows.rent_vehicle_widget import RentVehicleWidget


class AdminDialogController(QObject):
    def __init__(self, user, db_session, parent_window, logout_callback):
        super().__init__()
        self.current_user = user
        self.current_role = user.role.lower()
        self.db_session = db_session
        self.parent_window = parent_window
        self.logout_callback = logout_callback

        self.dialog = AdminDialog(user=user, session=db_session, controller=self)

        self.role_commands = {
            "admin": {
                "1": self.handle_add_seller_widget,
                "2": self.show_delete_seller_widget,
                "3": self.handle_register_widget,
                "4": self.show_delete_client_widget,
                "5": self.show_get_users_widget,
                "6": self.show_add_vehicle_widget,
                "7": self.show_remove_vehicle_widget,
                "8": self.show_get_vehicle_widget,
                "9": self.show_rent_vehicle_widget,
                "10": self.show_return_vehicle_widget,
                "11": self.show_repair_vehicle_widget,
                "12": self.show_update_user_widget
            },
            "seller": {
                "1": self.handle_register_widget,
                "2": self.show_delete_client_widget,
                "3": self.show_get_users_widget,
                "4": self.show_add_vehicle_widget,
                "5": self.show_remove_vehicle_widget,
                "6": self.show_get_vehicle_widget,
                "7": self.show_rent_vehicle_widget,
                "8": self.show_return_vehicle_widget,
                "9": self.show_repair_vehicle_widget,
                "10": self.show_update_user_widget
            },
            "client": {
                "1": self.show_get_vehicle_widget,
                "2": self.show_rent_vehicle_widget,
                "3": self.show_return_vehicle_widget,
                "4": self.show_update_user_widget
            }
        }

        self.dialog.command_selected.connect(self._handle_command_slot)
        self.dialog.logout.connect(self._handle_logout)

    def _handle_command_slot(self, command_num):
        print(f"{self.current_user=}, {self.current_role=}")
        """Wywołanie komendy w zależności od aktualnej roli użytkownika"""
        self._handle_command(self.current_role, command_num)

    def update_current_user(self, new_user):
        self.current_user = new_user
        self.current_role = new_user.role.lower()
        self.dialog.user = new_user
        print(f"✅ Zaktualizowano aktualnego użytkownika: {self.current_user.first_name} | rola: {self.current_role}")

    def show(self):
        self.dialog.showMaximized()
        self.dialog.raise_()
        self.dialog.activateWindow()

    def _handle_command(self, role, command_num):
        commands = self.role_commands.get(role)
        if not commands:
            print(f"❌ Nieznana rola użytkownika: {role}")
            return
        action = commands.get(command_num)
        if action:
            action()
        else:
            print(f"❌ Nieznana komenda: {command_num} dla roli {role}")

    def _handle_logout(self, user=None):
        self.dialog.close()
        if self.logout_callback:
            self.logout_callback()

    def show_widget(self, widget):
        layout = self.dialog.dynamic_area.layout()
        for i in reversed(range(layout.count())):
            w = layout.itemAt(i).widget()
            if w:
                w.setParent(None)
        layout.addWidget(widget)
        widget.show()
        print("✅ Widget dodany do dynamic_area")

# ------------------------------------------------------------------------------------------------------------------- #

    def handle_add_seller_widget(self):
        if self.dialog is None:
            print("❌ Błąd: AdminDialog nie został zainicjalizowany.")
            return
        view = RegisterUserView(parent=self.dialog, role="seller", auto=True)
        controller = RegisterUserController(self.db_session, view, parent_dialog=self.dialog)
        # view.set_controller(controller)
        self.controller = controller
        self.show_widget(view)

    def show_delete_seller_widget(self):
        print("🔧 Wywołano delete_client_widget() - MVC wersja")
        service = DeleteUsersService(session=self.db_session, role="seller")
        view = DeleteUsersWidget(role="seller")
        controller = DeleteUsersController(view, service)
        self.delete_seller_controller = controller
        self.show_widget(view)

    def handle_register_widget(self):
        if self.dialog is None:
            print("❌ Błąd: AdminDialog nie został zainicjalizowany.")
            return
        view = RegisterUserView(parent=self.dialog, role="client", auto=False)
        controller = RegisterUserController(self.db_session, view, parent_dialog=self.dialog)
        # view.set_controller(controller)
        self.controller = controller
        self.show_widget(view)

    def show_delete_client_widget(self):
        print("🔧 Wywołano delete_client_widget() - MVC wersja")
        service = DeleteUsersService(session=self.db_session, role="client")
        view = DeleteUsersWidget(role="client")
        controller = DeleteUsersController(view, service)
        self.delete_client_controller = controller
        self.show_widget(view)

    def show_get_users_widget(self):
        print("🔧 Wywołano show_get_users_widget()")
        service = GetUsersService(self.db_session)
        view = GetUsersWidget()
        controller = GetUsersController(view=view, service=service)
        self.get_users_controller = controller
        if self.dialog:
            self.dialog.load_widget(view)

    def show_add_vehicle_widget(self):
        print("🔧🔧🔧 Wywołano add_vehicle_widget()")
        view = AddVehicleView(self.current_role)
        controller = AddVehicleController(self.db_session, view, self.current_role)
        self.controller = controller
        self.show_widget(view)

        # self.add_vehicle_widget = AddVehicleWidget(self.db_session)
        # self.show_widget(self.add_vehicle_widget)

    def show_remove_vehicle_widget(self):
        print("🔧🔧🔧 Wywołano remove_vehicle_widget()")
        view = DeleteVehicleView()
        controller = DeleteVehicleController(self.db_session, view)
        self.controller = controller

        self.show_widget(view)

    def show_get_vehicle_widget(self):
        print("🔧🔧🔧 Uruchomiono repair_vehicle_widget()")
        role = self.current_user.role
        view = GetVehicleView(role=role)
        service = GetVehicleService(self.db_session, view)
        controller = GetVehicleController(view=view, session=self.db_session)
        self.controller = controller
        self.show_widget(view)

    def show_rent_vehicle_widget(self):
        print("🔧🔧🔧 Wywołano rent_vehicle_widget()")
        self.rent_vehicle_widget = RentVehicleWidget(self.db_session, self.current_user)
        self.show_widget(self.rent_vehicle_widget)

    def show_return_vehicle_widget(self):
        print("🔧🔧🔧 Wywołano return_vehicle_widget()")
        view = ReturnVehicleView(role="client")
        service = ReturnVehicleService(self.db_session, self.current_user)
        controller = ReturnVehicleController(self.db_session, view, service, self.current_user)
        view.set_controller(controller)
        self.show_widget(view)

    def show_repair_vehicle_widget(self):
        print("🔧🔧🔧 Uruchomiono repair_vehicle_widget()")
        view = RepairVehicleView()
        service = RepairService(self.db_session)
        controller = RepairController(view=view, session=self.db_session)
        self.repair_vehicle_controller = controller
        self.show_widget(view)

    def show_update_user_widget(self):
        print("🔧🔧🔧 Uruchomiono update_user_widget()")
        viev = UpdateUserView(self.current_user)
        controller = UpdateUserController(self.db_session, viev, self.current_user)
        self.controller = controller
        self.show_widget(viev)

    def show_overdue_rentals_widget(self):
        print("🔧🔧🔧 Uruchomiono overdue_rentals_widget()")
        view = OverdueRentalView(self.current_role)
        controller = OverdueRentalController(self.db_session, view, self.current_role)
        self.controller = controller
        self.show_widget(view)

        # self.overdue_vehicle_rentals = OverdueRentalsWidget(self.db_session, self.current_user)
        # self.show_widget(self.overdue_vehicle_rentals)

    def show_promo_banner_widget(self):
        print("🔧🔧🔧 Uruchomiono promo_banner_widget()")
        view = PromoBannerView()
        controller = PromoBannerController(self.db_session, view)
        self.controller = controller
        self.show_widget(view)

