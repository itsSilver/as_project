#!/usr/bin/python
# coding=utf-8


import json
import re
import web_util_0


class ModBetburger():


    def __init__(self, url, dir_url, bet_val_url, url_mid_name):
        self._url = url
        self._dir_url = dir_url 
        self._bet_val_url = bet_val_url
        self.url_mid_name = url_mid_name 


    # 获取页面所有的数据
    def get_data_info(self):
        url = self._url
        d = web_util_0.get_betburger_web_content(url)
        directories_data = web_util_0.get_directories(self._dir_url, self.url_mid_name)
        data = json.loads(d) 
        result = []
        bet_url_str = ''
        for a in data['arbs']:
            bets = {}
            bet1 = {}
            bet2 = {}
            bet3 = {}
            bets['percent'] = a['percent']
            bets['paused'] = a['paused']
            bets['middle_value'] = a['middle_value']
            sport_id = a['sport_id']
            sport_name = self.get_directory_data(sport_id, directories_data, dir_kw='sports', get_kw='name') 
            bets['sport'] = sport_name

            bet1_id = a['bet1_id']
            bet2_id = a['bet2_id']
            bet3_id = a['bet3_id']
            index1 = self.judge_index(bet1_id, data)
            index2 = self.judge_index(bet2_id, data)
            index3 = self.judge_index(bet3_id, data)

            bm_id_1 = data['bets'][index1]['bookmaker_id']
            bm_id_2 = data['bets'][index2]['bookmaker_id']
            bet1['bookmaker'] = self.get_directory_data(bm_id_1, directories_data, dir_kw='bookmakers', get_kw='name')
            bet2['bookmaker'] = self.get_directory_data(bm_id_2, directories_data, dir_kw='bookmakers', get_kw='name')

            bc_id1 = data['bets'][index1]['bc_id']
            bc_id2 = data['bets'][index2]['bc_id']
            bet1['bc_id'] = bc_id1
            bet2['bc_id'] = bc_id2
            bet_url_str += str(bc_id1) + ','
            bet_url_str += str(bc_id2) + ','

            bet1['home'] = data['bets'][index1]['home']
            bet1['away'] = data['bets'][index1]['away']
            bet1['league'] = data['bets'][index1]['league']
            bet1['current_score'] = data['bets'][index1]['current_score']
            bet1['market_depth'] = data['bets'][index1]['market_depth']
            bet1['koef'] = data['bets'][index1]['koef']
            bet1['created_at'] = data['bets'][index1]['created_at']
            bet1['updated_at'] = data['bets'][index1]['updated_at']
            bet1['started_at'] = data['bets'][index1]['started_at']
            
            bet2['home'] = data['bets'][index2]['home']
            bet2['away'] = data['bets'][index2]['away']
            bet2['league'] = data['bets'][index2]['league']
            bet2['current_score'] = data['bets'][index2]['current_score']
            bet2['market_depth'] = data['bets'][index2]['market_depth']
            bet2['koef'] = data['bets'][index2]['koef']
            bet2['created_at'] = data['bets'][index2]['created_at']
            bet2['updated_at'] = data['bets'][index2]['updated_at']
            bet2['started_at'] = data['bets'][index2]['started_at']

            # 牧鞭所有的bet3为空
            if index3 is not None:
                bet3['home'] = data['bets'][index3]['home']
                bet3['away'] = data['bets'][index3]['away']
                bet3['league'] = data['bets'][index3]['league']
                bet3['current_score'] = data['bets'][index3]['current_score']
                bet3['market_depth'] = data['bets'][index3]['market_depth']
                bet3['koef'] = data['bets'][index3]['koef']
                bet3['created_at'] = data['bets'][index3]['created_at']
                bet3['updated_at'] = data['bets'][index3]['updated_at']
                bet3['started_at'] = data['bets'][index3]['started_at']
                bets['bet3'] = bet3

            bets['bet1'] = bet1
            bets['bet2'] = bet2

            result.append(bets)

        bet_url_str = bet_url_str.rstrip(',')
        new_bet_val_url = self._bet_val_url + bet_url_str + '?access_token='
        bet_value_data = web_util_0.get_bet_value(new_bet_val_url)
        bet_combinations_data = bet_value_data['bet_combinations']
        bet_variations_data = directories_data['bet_variations']
        for res in result:
            bet1_break = False 
            bet2_break = False
            for bet in bet_combinations_data:
                if bet1_break == False:
                    if bet['id'] == res['bet1']['bc_id']:
                        res['bet1']['bet_value'] = bet['value']
                        res['bet1']['bv_id'] = bet['bv_id']
                        bet1_break = True
                if bet2_break == False:
                    if bet['id'] == res['bet2']['bc_id']:
                        res['bet2']['bet_value'] = bet['value']
                        res['bet2']['bv_id'] = bet['bv_id']
                        bet1_break = True
                if bet1_break == True and bet2_break == True:
                    break

            b1_break = False
            b2_break = False
            for d in bet_variations_data:
                if b1_break == False:
                    if res['bet1']['bv_id'] == d['id']:
                        res['bet1']['bet_variation_name'] = d['name']
                        b1_break = True
                if b2_break == False:
                    if res['bet2']['bv_id'] == d['id']:
                        res['bet2']['bet_variation_name'] = d['name']
                        b2_break = True
                if b1_break == True and b2_break == True:
                    break
    
        # print(result)
        return result


    # 获取目录对应的数据
    def get_directory_data(self, dir_id, dir_data, dir_kw, get_kw):
        if dir_data[dir_kw] != "":
            for d in dir_data[dir_kw]:
                if d['id'] == dir_id:
                    return d[get_kw]
        else:
            return ""


    # 判读每场比赛的索引位置
    def judge_index(self, bet_id, data):
        n = 0 
        for b in data['bets']:
            if b['id'] == bet_id:
                return n
            n += 1        


if __name__ == '__main__':
    urls = 'https://api-lv.betburger.com/api/v1/arbs/pro_search?access_token='
    dir_url = 'https://api-lv.betburger.com/api/v1/directories?access_token='
    bet_val_url = 'https://api-lv.betburger.com/api/v1/bet_combinations/'
    url_mid_name = 'betburger'
    mb = ModBetburger(urls, dir_url, bet_val_url, url_mid_name)
    mb.get_data_info()
