import sys, os
import pyrebase

sys.path.append(os.path.abspath("../diafano-vault/"))
credentials_file = "diafano-vault/credentials.py"

# import credentials for firebase
from credentials import export_credentials
config = export_credentials(None)

firebase_config = config['firebaseConfig']

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
database = firebase.database()
storage = firebase.storage()

#############################################
# TODO: find ways to make this faster, test on real data
#############################################

users = []
DUMMY = 100

def retrieveFScore(userid, followers):
	fList = []
	if followers :
		fList = database.child("followers").child(userid).get().val()
	else:
		fList = database.child("followings").child(userid).get().val()
	# check trust_rank into users child
	final_trust = 0 
	if fList != None:
		for friend in fList:
			final_trust += database.child("users").child(friend).child("trust_rank").get().val()
		return final_trust/len(fList)
	else: return 0

def calculateScores():
	users = database.child("users")

	for userid in users.get().val():
		previousRank = database.child("users").child(userid).child("trust_rank").get().val()
		newlyFoundRank = calculateScoreForSingleUser(userid)
		if previousRank == None: userRank = newlyFoundRank
		else: userRank = (float)(newlyFoundRank+previousRank)/2
		# push the result back if it changed at all

		if userRank != previousRank:
			database.child("users").child(userid).child("trust_rank").set(userRank) 

def normalizeScores(l):
	res = []
	for elem in l:
		if (max(l) - min(l)) != 0:
			res.append(100 * (elem - min(l))/(max(l) - min(l)) )
		else:
			res.append(100)
	return res

def calculateScoreForSingleUser(userid):	
	# retrieve all news from user in question
	try: newsList = database.child("news").order_by_child("author").equal_to(userid).get().val()
	except IndexError: return 0 # no news for this user

	newsScores = []
	totalNews = 0

	for newsId in newsList:
		newsScore = 0
		# upvote downvote contribution
		upvotes = database.child("news").child(newsId).child("upvotes").get().val()
		downvotes = database.child("news").child(newsId).child("downvotes").get().val()
		if upvotes == None: upvotes = 0
		if downvotes == None: downvotes = 0
		voteScore = upvotes - downvotes
		newsScore += (voteScore*DUMMY)

		# follower/followings score contribution
		followerScore = retrieveFScore(userid, True) # retrieve followers score
		followingScore = retrieveFScore(userid, False) # retrieve following score
		newsScore += (followingScore + followerScore)*DUMMY

		#sensitivity - increases score
		sens = database.child("news").child(newsId).child("possibly_sensitive").get().val()
		if sens != None: newsScore += 0.5*sens*newsScore

		# deacreases in score
		# misleading 
		misleading = database.child("news").child(newsId).child("misleading").get().val()
		if misleading: newsScore -= 0.25*newsScore

		violent = database.child("news").child(newsId).child("violent").get().val()
		if violent: newsScore -= 0.5*newsScore

		newsScores.append(newsScore)
		totalNews+= 1

	scoreList = normalizeScores(newsScores)	
	# print(newsScores, totalNews)
	s = 0
	for score in scoreList:
		s += score
	if totalNews == 0: return s
	return s/totalNews

calculateScores()
