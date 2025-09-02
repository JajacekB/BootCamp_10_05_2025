from repositories.read_methods import promo_banner_data


class PromoBannerController():
    def __init__(self, session, view):

        self.session =session
        self.view = view

        self.view.handle_promo_banner_data.connect(self.get_promo_banner_data)


    def get_promo_banner_data(self):

        time_promos, loyalty_promos = promo_banner_data(self.session)
        self.view.build_promo_banner(time_promos, loyalty_promos)
