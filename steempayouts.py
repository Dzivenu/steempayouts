from websocket import create_connection
from pprint import pprint
import json
import sys

ws = create_connection("ws://62.75.148.124:5090")

get_virtual_ops_api = {
    'method': 'call',
    'params': ['database_api', 'get_ops_in_block', []],
    'jsonrpc': '2.0',
    'id': '1'
}

author_board = {}
curator_board = {}
post_board = {}


def add_earning_author(author, earning):
    global author_board
    if author not in author_board.keys():
        author_board[author] = earning
    else:
        author_board[author]['sbd'] += earning['sbd']
        author_board[author]['vest'] += earning['vest']
        author_board[author]['steem'] += earning['steem']
        author_board[author]['post_num'] += 1


def add_earning_curator(curator, earning):
    global curator_board
    if curator not in curator_board.keys():
        curator_board[curator] = earning
    else:
        curator_board[curator]['reward_vest'] += earning['reward_vest']
        curator_board[curator]['unique_authors'].update(earning['unique_authors'])
        curator_board[curator]['votes_num'] += 1


def get_leaderboards_betweet_blocks(start_block, end_block):
    for block in range(start_block, end_block):
        get_virtual_ops_api['params'][2] = [block, 'true']
        get_virtual_ops = json.dumps(get_virtual_ops_api)
        ws.send(get_virtual_ops)
        result =  json.loads(ws.recv())
        for entry in result['result']:
            if entry['op'][0] == 'curation_reward':
                curator = entry['op'][1]['curator']
                reward = float(entry['op'][1]['reward'].split(' ')[0])
                comment_author = entry['op'][1]['comment_author']
                earning = {}
                earning['reward_vest'] = reward
                earning['unique_authors'] = {}
                earning['unique_authors'][comment_author] = 1
                earning['votes_num'] = 1
                add_earning_curator(curator, earning)
            elif entry['op'][0] == 'author_reward':
                author = entry['op'][1]['author']
                permlink = entry['op'][1]['permlink']
                sbd     = float(entry['op'][1]['sbd_payout'].split(' ')[0])
                vest    = float(entry['op'][1]['vesting_payout'].split(' ')[0])
                steem   = float(entry['op'][1]['steem_payout'].split(' ')[0])
                earning = {}
                earning['sbd'] = sbd
                earning['vest'] = vest
                earning['steem'] = steem
                earning['post_num'] = 1
                add_earning_author(author, earning)
                post_board['@{}/{}'.format(author, permlink)] = earning
            else:
                pass


########################################################################################################################
if __name__ == "__main__":
    if len(sys.argv) > 1:
        start_block = int(sys.argv[1])
        end_block = int(sys.argv[2])
        top = int(sys.argv[3])
    get_leaderboards_betweet_blocks(start_block, end_block)
    print("Top {} authors sorted by VESTS:".format(top))
    pprint(sorted(author_board.items(), key=lambda x:(x[1]['vest']), reverse=True)[0:top])
    print("Top {} curators sorted by VESTS:".format(top))
    pprint(sorted(curator_board.items(), key=lambda x:(x[1]['reward_vest']), reverse=True)[0:top])
    print("Top {} posts sorted by SBD:".format(top))
    pprint(sorted(post_board.items(), key=lambda x: (x[1]['sbd']), reverse=True)[0:top])

    ws.close()