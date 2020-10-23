from flask_restful import Resource
from flask import g, request, jsonify
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import config


class User(Resource):
    def post(self):
        try:
            data = request.json
            email = data["email"]
            # name = data["username"]
            now = datetime.now()
            dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
            cur = g.appdb.cursor()
            cur.execute("insert into user(user_name,password,created_at) value(%s,%s,%s)", (email, email, dt_string))
            g.appdb.commit()
            return jsonify({"status": "success", "response": "Mail created successfully"})
        except Exception as error:
            return jsonify({"status": "Error", "Response": str(error)})


class DraftMail(Resource):
    def post(self):
        try:
            cur = g.appdb.cursor()
            data = request.json
            subject = data["subject"]
            body = data["body"]
            sender = data["sender"]
            recipients = data["recipients"]
            created_by = data["created_by"]
            now = datetime.now()
            draft_at = str(now.strftime("%Y-%m-%d %H:%M:%S"))
            draft_query = """insert into email(subject,body,sender,\
                        recipients,created_by,created_at) values(%s,%s,%s,%s,%s,%s)"""
            cur.execute(draft_query, (subject, body, sender, str(recipients), created_by, draft_at))
            g.appdb.commit()
            return jsonify({"status": "Success", "Response": "Mail Draft Successfully"})

        except Exception as error:
            return jsonify({"Status": "Failed", "Response": str(error)})


class SendMail(Resource):
    def post(self):
        try:
            cur = g.appdb.cursor()
            now = datetime.now()
            dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
            data = request.json
            email_id = data['email_id']
            send_query = """SELECT u.mailid, e.subject, e.body,e.sender,e.recipients FROM \
                        email e INNER JOIN USER u ON u.id= e.created_by WHERE eid= %s"""
            cur.execute(send_query, (email_id))
            data = cur.fetchall()

            for reci in eval(data[0]['recipients']):
                now = datetime.now()
                sent_at = str(now.strftime("%Y-%m-%d %H:%M:%S"))
                try:
                    smtpserver = config.config.get("smtpserver")
                    smtpport = config.config.get("smtpport")
                    receipient = reci
                    msg = MIMEMultipart('alternative')
                    msg['Subject'] = data[0]['subject']
                    msg['From'] = data[0]['sender']
                    msg['To'] = reci
                    text = data[0]["body"]
                    part = MIMEText(text, 'plain')
                    msg.attach(part)
                    mail = smtplib.SMTP(smtpserver, smtpport)
                    mail.ehlo()
                    mail.starttls()
                    mail.login(config.config.get("email"), config.config.get("smtppass"))
                    mail.sendmail(config.config.get("email"), reci, msg.as_string())
                    mail.quit()

                    try:
                        status_query = """insert into email_status(email_id, recipient,status, sent_at)\
                                        values(%s, %s, %s, %s)"""
                        cur.execute(status_query, (email_id, reci, 'sent', sent_at))
                        g.appdb.commit()

                    except :
                        status_query = """insert into email_status(email_id,recipient,status, sent_at)\
                                        values(%s, %s, %s, %s)"""
                        cur.execute(status_query, (email_id, reci, 'pending', sent_at))
                        g.appdb.commit()

                except smtplib.SMTPException as e:
                    return jsonify({"status": "Failed", "Response": str(e)})
            return jsonify({'status': 'Success', 'response': 'mails have been sent successfully'})

        except Exception as error:
            return jsonify({"Status": "Failed", "Response": str(error)})


class GetEmailList(Resource):
    def get(self):
        try:
            cur = g.appdb.cursor()
            user_id = request.args.get("user_id", False)
            if user_id:
                cur.execute("SELECT * FROM email WHERE created_by= %s", user_id)
                data = cur.fetchall()
                return jsonify({"status": "success", "Response": data})
        except Exception as error:
            return jsonify({"status": "Failed", "Response": str(error)})


class EmailStatus(Resource):
    def get(self):
        try:
            cur = g.appdb.cursor()
            eid = request.args.get("eid", False)
            eid_query = """SELECT e.subject, e.body, e.sender, e.created_at, es.recipient,\
                        es.status, es.sent_at FROM email e INNER JOIN \
                        email_status es ON e.eid = es.email_id WHERE e.eid=%s"""
            if eid:
                cur.execute(eid_query, eid)
                data = cur.fetchall()
                return jsonify({"status": "success", "Response": data})
        except Exception as error:
            return jsonify({"status": "Failed", "Response": str(error)})


class EmailDetails(Resource):
    def get(self):
        try:
            cur = g.appdb.cursor()
            eid = request.args.get("eid", False)
            eid_query = """SELECT u.username, u.mailid, e.subject, e.body, e.sender, e.recipients,\
                            e.created_at FROM USER u INNER JOIN 
                            email e ON u.id = e.created_by WHERE e.eid=%s"""
            if eid:
                cur.execute(eid_query, eid)
                data = cur.fetchall()
                return jsonify({"status": "success", "Response": data})
        except Exception as error:
            return jsonify({"status": "Failed", "Response": str(error)})


class PendingMail(Resource):
    def get(self, action):
        cur = g.appdb.cursor()

        if action == "view":
            user_id = request.args.get("user_id", False)
            if user_id:

                view_query = """SELECT e.subject,e.body,e.sender,es.status,es.recipient FROM \
                                email e INNER JOIN email_status es ON
                                e.eid=es.email_id WHERE e.created_by = %s AND es.status='pending'"""
                cur.execute(view_query, user_id)
                data= cur.fetchall()
                return jsonify({"status": "success","Response":data})
            else:
                return jsonify({"status": "Failed","Response":"query parameter 'user id' is required"})

        if action == "resend":
            email_id= request.args.get("email_id", False)
            if email_id:
                view_query = """SELECT e.subject,e.body,e.sender,es.status,es.recipient,
                                e.recipients FROM email e INNER JOIN email_status es ON
                                e.eid=es.email_id WHERE e.eid = %s AND es.status='pending'"""
                cur.execute(view_query, email_id)
                data = cur.fetchall()
                if any(data):

                    for reci in eval(data[0]['recipients']):
                        now = datetime.now()
                        sent_at = str(now.strftime("%Y-%m-%d %H:%M:%S"))
                        try:
                            smtpserver = config.config.get("smtpserver")
                            smtpport = config.config.get("smtpport")
                            receipient = reci
                            msg = MIMEMultipart('alternative')
                            msg['Subject'] = data[0]['subject']
                            msg['From'] = data[0]['sender']
                            msg['To'] = reci
                            text = data[0]["body"]
                            part = MIMEText(text, 'plain')
                            msg.attach(part)
                            mail = smtplib.SMTP(smtpserver, smtpport)
                            mail.ehlo()
                            mail.starttls()
                            mail.login(config.config.get("email"), config.config.get("smtppass"))
                            mail.sendmail(config.config.get("email"), reci, msg.as_string())
                            mail.quit()
                            cur.execute("""UPDATE email_status SET STATUS = 'sent' WHERE email_id = %s;""",email_id)
                            g.appdb.commit()

                        except smtplib.SMTPException as e:
                            return jsonify({"status": "Failed", "Response": str(e)})
                else:
                    return jsonify({"status": "Failed", "Response": "No pending mail's on this mail id"})


                return jsonify({"status": "success","Response":data})
            else:
                return jsonify({"status": "Failed", "Response": "query parameter 'email id' is required"})
        else:
            return jsonify({"status": "Failed", "Response": "query parameter invalid"})

