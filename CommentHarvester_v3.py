import praw
from time import sleep, time
from sys import getsizeof
exit()
reddit = praw.Reddit(client_id='0QjUh0EpnKv5ww', client_secret='fpJAWvmwwIniJpmGYVkFMjTx-LI', user_agent='CommentHarvester:0QjUh0EpnKv5ww:1.0> (by /u/ShisukoDesu)')

def bar_print(s):
	print(s)
	print("---------------------------------------------------------------------------------------",flush=True)
def bar_write(s,writer):
	writer.write(s.encode('ascii','ignore').decode('ascii'))
	writer.write("\n---------------------------------------------------------------------------------------\n")
	writer.flush()
def data_write(subreddit_name,s,writer):
	writer.write('r/'+subreddit_name+'\n')
	writer.write(s)
	writer.flush()

def is_valid(s):
	invalid = ['[deleted]','[removed]']
	return False if len(s) <= 1 or s in invalid else True

last_call = time()
def harvest_comments(comment_len,comment_getsizeof,top_posts,DESIRED_COMMENT_COUNT,subreddit_name,comment_writer):
	global last_call
	harvest_count = 0 
	for submission in top_posts:	
		bar_print("Begin harvest from '"+submission.title+"'")
		bar_write("$$$$$ "+submission.title,comment_writer)
		
		submission.comments.replace_more(limit=50)
		last_call = time()
		local_harvest = 0
		
		
		for comment in submission.comments.list():
			if is_valid(comment.body):
				bar_write(comment.body,comment_writer)
				
				comment_len.append(len(comment.body))
				comment_getsizeof.append(getsizeof(comment.body))
				
				local_harvest += 1
				harvest_count += 1
				
				if harvest_count==DESIRED_COMMENT_COUNT:
					bar_print("Harvesting of r/" + subreddit_name + " is complete.")
					return
				if local_harvest==DESIRED_COMMENT_COUNT//5:
					break
					
		bar_print("{} out of {} comments harvested".format(harvest_count,DESIRED_COMMENT_COUNT))
		if time()-last_call <= 60:
			sleep(60-(time()-last_call))
				
subreddits_to_study = open('subreddits.txt','r').read().split()
data_len_writer = open('data/data_len.txt','w+')
data_getsizeof_writer = open('data/data_getsizeof.txt','w+')
start_time = time()
last_time = time()

for subreddit_name in subreddits_to_study:
	subreddit = reddit.subreddit(subreddit_name)
	comment_writer = open('actual_comments/r'+subreddit_name+'_comments.txt','w+')
	comment_len_writer = open('comment_len/r'+subreddit_name+'_comment_len.txt','w+')
	comment_getsizeof_writer = open('comment_getsizeof/r'+subreddit_name+'_comment_len.txt','w+')
	'''
		Acquire 5000 comments from Top, and 5000 comments from Controversial
		For each submission, take up to 1000 non-deleted comments
	'''
	DESIRED_COMMENT_COUNT = 10000
	comment_len = []
	comment_getsizeof = []
	
	bar_print("Harvesting comments from r/"+subreddit_name)
	
	harvest_comments(comment_len,comment_getsizeof,subreddit.top(),DESIRED_COMMENT_COUNT,subreddit_name,comment_writer)
	
	s_len = ','.join([str(x) for x in comment_len])+'\n'
	s_getsizeof = ','.join([str(x) for x in comment_getsizeof])+'\n'
	
	comment_len_writer.write(s_len)
	comment_getsizeof_writer.write(s_getsizeof)
	data_write(subreddit_name,s_len,data_len_writer)
	data_write(subreddit_name,s_getsizeof,data_getsizeof_writer)
	
	print("{} minutes have elapsed since program start.".format((time()-start_time)/60))
	bar_print("{} minutes were used to process this subreddit.".format((time()-last_time)/60))
	last_time = time()

	comment_writer.close()
	comment_len_writer.close()
	comment_getsizeof_writer.close()

data_len_writer.close()
data_getsizeof_writer.close()