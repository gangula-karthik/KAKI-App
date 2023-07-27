from flask import Flask, render_template
import firebase_admin
from firebase_admin import credentials, db


def get_all_reports():
    reports = {}

    categories = ["Transactions", "Individual", "Community"]

    reports_ref_trans = db.reference("/Users/Saved_report/Transactions")
    reports_snapshot_t = reports_ref_trans.get()

    reports_ref_indi = db.reference("/Users/Saved_report/Individual")
    reports_snapshot_i = reports_ref_indi.get()

    reports_ref_com = db.reference("/Users/Saved_report/Community")
    reports_snapshot_c = reports_ref_com.get()

    reports.update(reports_snapshot_c)
    reports.update(reports_snapshot_i)
    reports.update(reports_snapshot_t)



    return reports




