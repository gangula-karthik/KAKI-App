
class Saved_Report:
    report_id_count = 0
    def __init__(self,id):
        self.__report_id__= id


class Indi_Report(Saved_Report):

    def __init__(self):

        Saved_Report.report_id_count+=1
        super().__init__(Saved_Report.report_id_count)
        self.__report_id__ =Saved_Report.report_id_count
        self.__leaderboard__ = None
        self.__CurrentMonth__=None
        self.__CurrentYear__=None
        self.__listMonths__=None
        self.__lineData__=None
        self.__pieData__=None
        self.__neighboursHelped__=None
        self.__activities__=None
        self.__pieLabel__=None

    def get_report_id(self):
        return self.__report_id__

    def get_leaderboard(self):
        return self.__leaderboard__

    def get_current_month(self):
        return self.__CurrentMonth__

    def get_current_year(self):
        return self.__CurrentYear__

    def get_list_months(self):
        return self.__listMonths__

    def get_line_data(self):
        return self.__lineData__

    def get_pie_data(self):
        return self.__pieData__

    def get_neighbours_helped(self):
        return self.__neighboursHelped__

    def get_activities(self):
        return self.__activities__

    def get_pie_label(self):
        return self.__pieLabel__

    # Setter methods
    def set_leaderboard(self, leaderboard):
        self.__leaderboard__ = leaderboard

    def set_current_month(self, month):
        self.__CurrentMonth__ = month

    def set_current_year(self, year):
        self.__CurrentYear__ = year

    def set_list_months(self, months_list):
        self.__listMonths__ = months_list

    def set_line_data(self, line_data):
        self.__lineData__ = line_data

    def set_pie_data(self, pie_data):
        self.__pieData__ = pie_data

    def set_neighbours_helped(self, neighbours_helped):
        self.__neighboursHelped__ = neighbours_helped

    def set_activities(self, activities):
        self.__activities__ = activities

    def set_pie_label(self, pie_label):
        self.__pieLabel__ = pie_label


class Com_Report(Saved_Report):

    def __init__(self):
        Saved_Report.report_id_count += 1
        super().__init__(Saved_Report.report_id_count)
        self.__report_id__ = Saved_Report.report_id_count
        self.__leaderboard__ = None
        self.__CurrentMonth__ = None
        self.__CurrentYear__ = None
        self.__listMonths__ = None
        self.__lineData__ = None
        self.__pieData__ = None
        self.__MostContributed__ = None
        self.__activities__ = None
        self.__pieLabel__ = None

    def get_report_id(self):
        return self.__report_id__

    def get_leaderboard(self):
        return self.__leaderboard__

    def get_current_month(self):
        return self.__CurrentMonth__

    def get_current_year(self):
        return self.__CurrentYear__

    def get_list_months(self):
        return self.__listMonths__

    def get_line_data(self):
        return self.__lineData__

    def get_pie_data(self):
        return self.__pieData__

    def get_MostContributed(self):
        return self.__MostContributed__

    def get_activities(self):
        return self.__activities__

    def get_pie_label(self):
        return self.__pieLabel__

    # Setter methods
    def set_leaderboard(self, leaderboard):
        self.__leaderboard__ = leaderboard

    def set_current_month(self, month):
        self.__CurrentMonth__ = month

    def set_current_year(self, year):
        self.__CurrentYear__ = year

    def set_list_months(self, months_list):
        self.__listMonths__ = months_list

    def set_line_data(self, line_data):
        self.__lineData__ = line_data

    def set_pie_data(self, pie_data):
        self.__pieData__ = pie_data

    def set_MostContributed(self, MostContributed):
        self.__MostContributed__ = MostContributed

    def set_activities(self, activities):
        self.__activities__ = activities

    def set_pie_label(self, pie_label):
        self.__pieLabel__ = pie_label


class trans_report(Saved_Report):
    def __init__(self):
        Saved_Report.report_id_count += 1
        super().__init__(Saved_Report.report_id_count)
        self.__transactionDataIn__ =None
        self.__transactionDataOut__ = None
        self.__NoTransactionData = None

    def get_transaction_data_in(self):
        return self.__transactionDataIn__

    def get_transaction_data_out(self):
        return self.__transactionDataOut__

    def get_no_transaction_data(self):
        return self.__NoTransactionData

    # Setter methods
    def set_transaction_data_in(self, transaction_data_in):
        self.__transactionDataIn__ = transaction_data_in

    def set_transaction_data_out(self, transaction_data_out):
        self.__transactionDataOut__ = transaction_data_out

    def set_no_transaction_data(self, no_transaction_data):
        self.__NoTransactionData = no_transaction_data


class events_report():
    def __init__(self):
        self.__event_name__ =None
        self.__event_date = None
        self.__venue__ = None
        self.__event_description__ = None
        self.__time__ = None
        self.__overall_in_charge__ = None
        self.__dateposted__ = None

    def get_event_name(self):
        return self.__event_name__

    def get_event_date(self):
        return self.__event_date__

    def get_venue(self):
        return self.__venue__

    def get_event_description(self):
        return self.__event_description__

    def get_time(self):
        return self.__time__

    def get_overall_in_charge(self):
        return self.__overall_in_charge__

    def get_date_posted(self):
        return self.__dateposted__

    # Setter methods
    def set_event_name(self, event_name):
        self.__event_name__ = event_name

    def set_event_date(self, event_date):
        self.__event_date__ = event_date

    def set_venue(self, venue):
        self.__venue__ = venue

    def set_event_description(self, event_description):
        self.__event_description__ = event_description

    def set_time(self, time):
        self.__time__ = time

    def set_overall_in_charge(self, overall_in_charge):
        self.__overall_in_charge__ = overall_in_charge

    def set_date_posted(self, date_posted):
        self.__dateposted__ = date_posted

