import smtplib

import requests
from bs4 import BeautifulSoup
from random import SystemRandom


class Sbpdcl(object):

    @staticmethod
    def get_random_user_agent():
        user_agents = [
            "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.8) Gecko/20071008 Firefox/2.0.0.8",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.7) Gecko/20070914 Firefox/2.0.0.7",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.4) Gecko/20070515 Firefox/2.0.0.4",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.0 (KHTML, like Gecko) Chrome/3.0.183.1 Safari/531.0",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.0 (KHTML, like Gecko) Chrome/3.0.187.1 Safari/531.0",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.1 Safari/532.0",
            "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/531.3 (KHTML, like Gecko) Chrome/3.0.193.2 Safari/531.3",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.17 Safari/532.0",
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",
            "Opera/9.22 (Windows NT 5.1; U; en)",
            "Opera/9.24 (Windows NT 5.1; U; en)",
            "Opera/9.23 (Windows NT 5.1; U; en)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; InfoPath.1)",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0"
        ]
        return SystemRandom().choice(user_agents)

    def get_form_data(self, soup, more=dict()):
        fields = dict()
        for field in soup.find_all("input"):
            try:
                fields[field["name"]] = field["value"]
            except:
                fields[field["name"]] = ""
        for field in soup.find_all("select"):
            fields[field["name"]] = ""
        for field in soup.find_all("textarea"):
            fields[field["name"]] = field.string
        fields.update(more)
        return fields

    def modify_input(self, form_data, delete_values, modify_values, add_values):
        for d in delete_values:
            form_data.pop(d, None)
        form_data.update(modify_values)
        form_data.update(add_values)
        return form_data

    @staticmethod
    def parse_table_vertical(table_tag):
        if table_tag.find('tbody'):
            table_tag = table_tag.find('tbody')
        tr_tag_list = table_tag.find_all("tr")
        header_tag, tr_tag_list = tr_tag_list[0], tr_tag_list[1:]
        camel_case = lambda s: s[:1].lower() + s[1:] if s else ''
        header = [camel_case(th.text.strip().title().replace(" ", "")) for th in header_tag.find_all("th")]
        documents = []
        for tr in tr_tag_list:
            lists = dict(zip(header, [td.text.strip() for td in tr.find_all("td", recursive=False)]))
            documents.append(lists)
        return documents

    @staticmethod
    def send_mail(subject, body, recipient):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("fascinatemeok@gmail.com", "mfztfuhutbimfszn")
        subject = subject
        body = body
        msg = f"Subject : {subject} \n\n {body}"
        server.sendmail(
            "fascinatemeok@gmail.com",
            recipient,
            msg
        )
        print("Email sent !")
        server.quit()

    @staticmethod
    def parse_table_horizontal(table_tag):
        if table_tag.find('tbody'):
            table_tag = table_tag.find('tbody')
        tr_tag_list = table_tag.find_all("tr")
        values = []
        headers = []
        for tr in tr_tag_list:
            if tr.find("input", {"type": "text"}):
                td_tag_list = tr.find_all("td")
                for i, td in enumerate(td_tag_list):
                    input_type_text = td.find("input", {"type": "text"})
                    if input_type_text:
                        values.append(input_type_text.get("value", ""))
                        headers.append(td_tag_list[i - 1].text.strip())
        data = dict(zip(headers, values))
        print("Data:", data)
        return {
            "consumerName": data["Consumer Name"],
            "mobile_number": data["Mobile No"],
            "netPayableBeforeDueDate": data["Rechargable Amount"]
        }

    def get_details(self, metadata):
        consumer_no = metadata.get("consumer_no")
        for i in range(5):
            r = requests.Session()
            headers = {
                'User-Agent': self.get_random_user_agent()
            }
            response = r.get("https://sbpdcl.co.in", headers=headers, verify=False)
            base_url = response.url.split(")/")[0] + ")"
            url = '{}/frmQuickBillPaymentAll.aspx'.format(base_url)
            try:
                q = r.get(url, verify=False)
                newurl = q.url
            except Exception as e:
                print(e)
                continue
            if q.status_code == 200:
                soup = BeautifulSoup(q.text, "html.parser")
                form_data = self.get_form_data(soup)
                form_data = self.modify_input(form_data, [
                    "ctl00$MainContent$btnRural",
                    "ctl00$MainContent$btnCloseCANo",
                    "ctl00$MainContent$drpRSubDiv",
                    "ctl00$bttHome",
                    "ctl00$btnSearch",
                    "ctl00$bttSitemap"
                ], {
                                                  "ctl00$MainContent$rbtnSearch": "1",
                                                  "ctl00$MainContent$drpRdivision": "0",
                                                  "ctl00$MainContent$txtCANO": consumer_no,
                                              }, {
                                                  "__EVENTARGUMENT": "",
                                                  "__LASTFOCUS": "",
                                                  "__EVENTTARGET": ""
                                              })

                headers = {
                    'User-Agent': self.get_random_user_agent(),
                    'Host': 'sbpdcl.co.in',
                    'Referer': url,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
                print("Hitting New URL")
                try:
                    q1 = r.post(newurl, data=form_data, headers=headers, verify=False)
                except Exception as e:
                    print(e)
                    continue
                if q1.status_code == 200:
                    if 'Invalid CA Number' in q1.text or 'Bill details are not available for CA Number' in q1.text \
                            or 'CA Number does not belong to' in q1.text or \
                            "Non-Energy Payment details are not available for Temporary Registration Number" in q1.text:
                        return 'NO_RECORD_FOUND'
                    soup = BeautifulSoup(q1.text, "html.parser")
                    tab = soup.find('table', attrs={'id': 'MainContent_GVBillDetails'})
                    results = {}
                    # try:
                    #     if tab:
                    #         data = self.parse_table_vertical(tab)
                    #     else:
                    #         tab2 = soup.find("div", attrs={"id": "MainContent_pnlTotalAmountText"}).find("table")
                    #         data = self.parse_table_horizontal(tab2)
                    # except Exception as e:
                    #     print(e)
                    #     continue
                    # if not data:
                    #     print(q1.text)
                    # if isinstance(data, list):
                    #     results.update(data[0])
                    # elif isinstance(data, dict):
                    #     results.update(data)
                    # results.update(self.extract_info(soup))
                    # PARSE PDF
                    if soup.find("input", {"id": "MainContent_GVBillDetails_lnkView_0"}):
                        form_data = self.get_form_data(soup)
                        form_data = self.modify_input(form_data,
                                                      [
                                                          "ctl00$MainContent$btnCloseCANo",
                                                          "ctl00$MainContent$btnConfirmPay",
                                                          "ctl00$MainContent$rbtnlstPaymode",
                                                          "ctl00$MainContent$btnShowPopup",
                                                          "ctl00$btnSearch",
                                                          "ctl00$MainContent$drpRSubDiv",
                                                          "ctl00$bttSitemap",
                                                          "ctl00$MainContent$GVBillDetails$ctl02$lnkPay",
                                                          "ctl00$MainContent$btnRural",
                                                          "ctl00$bttHome",
                                                          "ctl00$MainContent$btnSubmit"
                                                      ],
                                                      {
                                                          "ctl00$MainContent$drpRdivision": "0",
                                                          "ctl00$MainContent$rbtnSearch": "1"
                                                      },
                                                      {})

                        headers = {
                            'User-Agent': self.get_random_user_agent(),
                            'Host': 'sbpdcl.co.in',
                            'Referer': url,
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Content-Type': 'application/x-www-form-urlencoded',
                        }
                        try:
                            response = r.post(newurl, data=form_data, headers=headers, verify=False, stream=True)
                        except Exception as e:
                            print(e)
                            continue
                    elif soup.find("input", {"id": "MainContent_lnkView1"}):
                        adv_url = '{}/frmAdvBillPaymentAll.aspx'.format(base_url)

                        form_data1 = self.get_form_data(soup)
                        form_data1 = self.modify_input(form_data1,
                                                       [
                                                           "ctl00$MainContent$btnCloseCANo",
                                                           "ctl00$MainContent$btnConfirmPay",
                                                           "ctl00$MainContent$rbtnlstPaymode",
                                                           "ctl00$btnSearch",
                                                           "ctl00$bttSitemap",
                                                           "ctl00$bttHome",
                                                           "ctl00$MainContent$btnSubmit",
                                                           "ctl00$MainContent$btnClose",
                                                           "ctl00$MainContent$btnCurrentblnce"
                                                       ],
                                                       {},
                                                       {
                                                           "ctl00$MainContent$lnkView1": "View Bill",
                                                           "ctl00$MainContent$txtConID": consumer_no,
                                                           "ctl00$MainContent$txtConName": "PINKI  RANI",
                                                           "ctl00$MainContent$txtAmountPayable": "",
                                                           "ctl00$MainContent$txtEmailId": "",
                                                           "ctl00$MainContent$txtMobileNo": "",
                                                           "ctl00$MainContent$txtCurrentblnce": "",
                                                           "__EVENTARGUMENT": "",
                                                           "__LASTFOCUS": "",
                                                           "__EVENTTARGET": ""
                                                       })

                        headers = {
                            'User-Agent': self.get_random_user_agent(),
                            'Host': 'sbpdcl.co.in',
                            'Referer': adv_url,
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Content-Type': 'application/x-www-form-urlencoded',
                        }
                        try:
                            response = r.post(adv_url, data=form_data1, headers=headers, verify=False, stream=True)
                        except Exception as e:
                            print(e)
                            continue

                        soup = BeautifulSoup(response.text, "html.parser")
                        VIEWSTATE = soup.find('input', attrs={'id': '__VIEWSTATE'}).get("value")
                        VIEWSTATEGENERATOR = soup.find('input', attrs={'id': '__VIEWSTATEGENERATOR'}).get("value")
                        EVENTVALIDATION = soup.find('input', attrs={'id': '__EVENTVALIDATION'}).get("value")

                        form_data_new = {
                            "__EVENTTARGET": "",
                            "__EVENTARGUMENT": "",
                            "__LASTFOCUS": "",
                            "__VIEWSTATE": VIEWSTATE,
                            "__VIEWSTATEGENERATOR": VIEWSTATEGENERATOR,
                            "__EVENTVALIDATION": EVENTVALIDATION,
                            "ctl00$MainContent$txtConID": "102219722",
                            "ctl00$MainContent$txtConName": "PINKI RANI",
                            "ctl00$MainContent$txtAmountPayable": "",
                            "ctl00$MainContent$btnCurrentblnce": "Get Current Balance",
                            "ctl00$MainContent$txtEmailId": "",
                            "ctl00$MainContent$txtMobileNo": "",
                            "ctl00$MainContent$txtCurrentblnce": ""
                        }

                        try:
                            response = r.post(adv_url, data=form_data_new, headers=headers, verify=False, stream=True)
                        except Exception as e:
                            print(e)
                            continue
                        soup = BeautifulSoup(response.text, "html.parser")
                        current_balance = soup.find('input', attrs={'name': 'ctl00$MainContent$txtCurrentblnce'}) \
                            .get("value")
                        print(current_balance)
                        if float(current_balance) > 75:
                            self.send_mail(
                                "Updated Electricity Balance",
                                "Balance = {}".format(current_balance),
                                ["priyakamta007@gmail.com", "deekshaseth1995@gmail.com"]
                            )
                        else:
                            self.send_mail(
                                "Electricity Recharge Needed!",
                                "Balance = {}".format(current_balance),
                                ["iamsanketkamta@gmail.com", "priyakamta007@gmail.com"]
                            )
                        break

    @staticmethod
    def extract_info(soup):
        total_amount = soup.find("input", {"id": "MainContent_txtAmountPayable"}).get("value")
        email_id = soup.find("input", {"id": "txtEmailId"}).get("value")
        mobile_number = soup.find("input", {"id": "txtMobileNo"}).get("value")
        return {
            "total_amount": total_amount if total_amount else "",
            "email_id": email_id if email_id else "",
            "mobile_number": mobile_number if mobile_number else ""
        }


Sbpdcl().get_details({"consumer_no": "102219722"})
