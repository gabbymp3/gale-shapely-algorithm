
"""

The Gale-Shapely algorithm is an algorithm that, 
given two non-overlapping groups, group A and group B,
and each group members preference for the members of the other group
makes pairings of A and B members, so that no two people would both 
be happier if they switched partners with each other.



"""

import random
import time
import math




class Student: 
	"""
	A class to represent a student and their preferences for partner
	** Review https://www.programiz.com/python-programming/class
	if you don't know how to specify methods in a class **
	
	Attributes
	----------
	group(Group): the Group that this student belongs to
		Useful for looking up group members by name in order to propose to them
	
	name(str): the (unique) name for this student
	
	partner_ratings(list of str): a list of the names of all students in the 
		other group, sorted by how much this student prefers them
		NOTE: THIS IS ORDERED FROM LEAST TO MOST PREFERED 

	
	partner(Student): this student's current partner
		starts as None until we reset it with reset_partnerships

	to_propose(list of str): 
		Added by create_gale_shapely_partnerships.
		Class attributes can be added by any function, 
		not just in init or methods

	...
	"""

	def randomize_ratings(self):
		""" Randomizes this student's preferences. 
		Useful for testing and running random experiments """
		random.shuffle(self.partner_ratings)






	def __init__ (self, group, name, partner_ratings):
		self.group = group
		self.name = name
		self.partner_ratings = partner_ratings
		self.partner = None





	def __str__(self):
		partner_name = self.partner.name if self.partner else "no-one"
		return f"{self.name} ({partner_name})"



	""" returns True if has a partner, False otherwise """

	def has_partner(self):
		return self.partner is not None
	



	# Given a name, return how much this student wants to work with 
	#	the student by that name (**higher numbers are better**)
	# Given a name, return their index in the ratings

	def get_rating_of_name(self,name):
		return self.partner_ratings.index(name)



	# 	If there is no current partner, return -1,
	# 		Otherwise, return our rating for our current partner
	
	
	def get_rating_of_current_partner(self):
		if self.has_partner():
			return self.get_rating_of_name(self.partner.name)
		return -1

	
	

	# 	If we have a partner, set our partner's partner to None
	# 	then set our partner to None


	def break_partnership(self):
		if self.has_partner():
			self.partner.partner = None
			self.partner = None

	

	# 	Form a partnership with this person
	#	If the new_partner already has a partner, we need to break them up
	#	If we already have a partner, we need to break up, too
	#	Then set this person as our partner, and set us as this person's partner


	def make_partnership(self, new_partner):
		if new_partner.has_partner() or self.has_partner():
			new_partner.break_partnership()
			self.break_partnership()
		self.partner = new_partner
		new_partner.partner = self





	# This student is going to propose a partnership with their 
	# 	current top choice (who has not already rejected them)


	# 	consider three outcomes:
	# 	- this potential partner does not have a partner yet
	# 		- they accept the proposal, make the partnership			
	# 	- they *do* have a partner
	# 		- if we are more preferred, they accept the proposal 
	# 			and break up with their current partner
	# 			- make the partnership
	# 		- if we are lower, nothing happens, but they are now 
	# 			removed from our list of potential partners (with "pop")
	#			so we can't propose to them again


	def propose_to_top_choice(self):
		current_top_choice = self.to_propose.pop()
		top_choice_object = self.group.get_student_by_name(current_top_choice)

		if top_choice_object.partner == None:
			self.make_partnership(top_choice_object)
		
		elif top_choice_object.get_rating_of_current_partner() < top_choice_object.get_rating_of_name(self.name):
			self.make_partnership(top_choice_object)

		return None
	
class Group: 
	"""
	Contains two groups of students, and methods for match-making

	Attributes:
		all_students: 	(list of Student)
		students_a: 	(list of Student) just the students in Group A
		students_b: 	(list of Student) just the students in Group B
	"""

	def __init__(self, names_a, names_b):
		
		self.students_a = []
		self.students_b = []
		
		# For ratings, start everyone with randomly shuffled ratings
		for name in names_a:

			ratings = names_b[:]
			random.shuffle(ratings)
			self.students_a.append(Student(self, name, ratings))
		
		for name in names_b:
			ratings = names_a[:]
			random.shuffle(ratings)
			self.students_b.append(Student(self, name, ratings))

		self.all_students = self.students_a + self.students_b

	def get_student_by_name(self, name):
		""" 
		Given a name, return the student with that name
		Parameters:
			name (str)
		Returns
			Student (the student with that name)
			or None if not found
		"""
		
		found = [s for s in self.all_students if s.name == name]
		if len(found):
			return found[0]
		return None


	def set_ratings(self, ratings):
		""" 
		Given a dictionary of name:ranking pairs, 
		set each student's preferences to these partner rankings
		"""
		for (name, partner_ratings) in ratings.items():
			s = self.get_student_by_name(name)
			s.partner_ratings = partner_ratings



	def randomize_ratings(self):
		""" 
		Randomize all the preferences, used for running experiments 
		"""
		[s.randomize_ratings() for s in self.all_students]



	def break_all_partnerships(self):
		""" Remove all partnerships from this group """
		for s in self.all_students:
			s.break_partnership()


	def make_naive_partnerships(self):
		"""
		Make not-very good partnerships by pairing up the first person 
		in group_a with the first person in group_b... etc

		Breaks up all partnerships first
		Returns None
		"""

		# make naive partnerships for each student in group_a
	
		self.break_all_partnerships()
		for i, student_a in enumerate(self.students_a):
			student_b = self.students_b[i]
			student_a.make_partnership(student_b)

		return None


	def make_gale_shapely_partnerships(self):

		"""
		Make partnerships with the Gale Shapely algorithm
		This should result in better partnerships than the naive approach
		"""

		self.break_all_partnerships()
		for student in self.students_a:
			student.to_propose = student.partner_ratings[:]
		
		for student in self.students_a:
			student.propose_to_top_choice()
		
		while len(self.get_unpartneredA()) > 0:
			for student in self.get_unpartneredA():
				student.propose_to_top_choice()


	
		# 	First, break all existing partnerships
		#	Group A is the proposers
		#  		Add a to_propose list to each student in group A
		#			which is a *copy* of the partner_ratings list for that student. 
		#			We will be *removing* names from it, so we want a copy, not a reference
		#
		# 	While there are any unpartnered proposers left:
		#		Each unpartnered proposer offers to their top choice partner
		#			That partner may accept or not (that is handled by offer_to_top_choice) 
		#		Eventually, if the algoritm is implemented correctly, 
		#		everyone will be partnered
	
		return None
	
	def get_unpartneredA(self):
		unpartnered = [s for s in self.students_a if not s.has_partner()]
		return unpartnered

	#-------------------------------
	# Useful data-printing methods
	
	def print_partnership_quality(self):
		
		partnerships = [(a,a.partner) for a in self.students_a if a.partner]

		# Keep track of how happy A and B are
		for (a, b) in partnerships:
			a_happy = a.get_rating_of_current_partner()
			b_happy = b.get_rating_of_current_partner()
			print(f"{a.name:10}({a_happy}) {b.name:10}({b_happy})") 

		unpartnered = [s for s in self.all_students if not s.has_partner()]
		
		print("Unpartnered: " + ", ".join([str(s) for s in unpartnered])) 

		print(f"Group A happiness = {calculate_average_happiness(self.students_a)}")
		print(f"Group B happiness = {calculate_average_happiness(self.students_b)}")
		print(f"  Total happiness = {calculate_average_happiness(self.all_students)}")


	def print_student_information(self):
		all_students = self.students_a + self.students_b

	
		print("\nAll students: ")
		for s in all_students:
			print(f"\t{str(s).ljust(30)} happiness: {s.get_rating_of_current_partner()}, ratings: {','.join(s.partner_ratings)}")


#-----------
# Experiment-running functions

def calculate_average_happiness(students):
	happiness_per_person = [s.get_rating_of_current_partner() for s in students]
	total = sum(happiness_per_person)

	option_count = len(students[0].partner_ratings) - 1
	student_count = len(students)
	return total/(student_count*option_count)



def run_experiment(student_count=10, run_count=10, matchmaking_fxn="make_gale_shapely_partnerships"):
	"""
	Run an experiment
	
	Create a Group of student_count pairs of Students

	Run run_count times:
		randomize the group's ratings
		call the correct method on the group
		calculate and add the total happiness for group A, B and all students
	
	Parameters:
		student_count(int): how many students to create
		run_count(int): how many times to run the matchmaking algorithm
		matchmaking_fxn(str): the name of the method to use for matchmaking
	Returns
		A dictionary representing unfairness, time-per-matchmaking, 
			average happiness, and the experiment parameters that were passed in
		dict {"matchmaking_fxn","student_count", "run_count" "a", "b", "all", "unfairness", "time"}

	"""


	names_a = ["A" + str(i) for i in range(0,student_count)]
	names_b = ["B" + str(i) for i in range(0,student_count)]
	g = Group(names_a, names_b)

	total_happiness_a = 0
	total_happiness_b = 0
	total_happiness = 0

	total_time = 0


	# How happy is everyone *on average?*
	# How long does it take *on average?*


	start_time = time.perf_counter()
	for i in range(run_count):
		g.randomize_ratings()
		if matchmaking_fxn is 'make_gale_shapely_partnerships':
			g.make_gale_shapely_partnerships()
		
		elif matchmaking_fxn is 'make_naive_partnerships':
			g.make_naive_partnerships()
		
		total_happiness_a += calculate_average_happiness(g.students_a)
		total_happiness_b += calculate_average_happiness(g.students_b)
		total_happiness += calculate_average_happiness(g.all_students)
		
	end_time = time.perf_counter()
	total_time = (end_time - start_time)/run_count





	# We measure unfairness as the ratio of how much happier A is than B
	unfairness = total_happiness_a/total_happiness_b

	# Return the results
	return {
		"matchmaking_fxn": matchmaking_fxn,
		"student_count": student_count,
		"run_count": run_count,
		"a": total_happiness_a/run_count, # Average over *all runs*
		"b": total_happiness_b/run_count,
		"all": total_happiness/run_count,
		"unfairness": unfairness,
		"time": total_time*1000, # Convert to milliseconds not seconds
	}


if __name__ == '__main__':

	# ******************************************************
	# ******************************************************


	print("-"*50 + "\nTest basic student creation\n")

	
	# Create some test students, with names and rankings of prefered partners
	s0 = Student(None, "Jason", ["Rachael", "Ryan", "Riley", "Richard"])
	s1 = Student(None, "Joy", ["Rachael", "Ryan", "Richard", "Riley"])
	s2 = Student(None, "Ryan", [ "Joy", "Jeremiah","Jason", "Jessica"])
	s3 = Student(None, "Riley", ["Jason", "Joy", "Jeremiah", "Jessica"])

	
	# # Set these two as partners
	s0.partner = s2
	s2.partner = s0

	# Test Task 0:
	assert s0.name == "Jason", "Did you store the Student's name?"
	assert s0.partner_ratings[0] == "Rachael", f"Did you store the Student's ratings, if provided?"

	# Test Task 1:
	print("Stringify Jason:", str(s0))
	print("Stringify Riley:", str(s3))
	assert str(s0) == "Jason (Ryan)", "__str__ not implemented correctly"
	assert str(s3) == "Riley (no-one)", "__str__ not implemented correctly"


	# Test Task 2:
	assert s2.has_partner() == True, "has_partner returns False even if there is a partner"
	assert s1.has_partner() == False, "has_partner returns True even if there isn't a partner"

	# Test Task 3:
	assert s2.get_rating_of_name("Jessica") == 3, "Ryan should rank Jessica as 3 (top choice!)"
	
	# Test Task 4:
	assert s0.get_rating_of_current_partner() == 1, "Jason should rank their current partner Ryan as 1 (not very good)"
	assert s1.get_rating_of_current_partner() == -1, "Joy doesn't have a partner, should return 0"
	
	
	# #-----------------
	# # Partner swapping
	print("-"*50 + "\nTest students methods for setting partnerships\n")
	
	# # Test Task 5:
	s0.break_partnership()
	assert not s0.has_partner(), "Remove partnership not working"
	assert not s2.has_partner(), "Remove partnership not working. Remember to remove the partner's partner as well"

	# # Test Task 6:
	# # Jason partners with Riley
	s0.make_partnership(s3)
	print(f"After making Jason and Riley partners:\m {s0}, {s3}")
	assert f"{s0} {s3}" == "Jason (Riley) Riley (Jason)", "Make partnership not working"
	
	# # Riley partners with Joy, breaking up with Jason
	s3.make_partnership(s1)
	print(f"After Riley dumps Jason for Joy:\n {s1}, {s3}, {s0}")
	assert not s0.has_partner(), "Remove partnership not working"
	
	# # Riley partners back with Jason, breaking up with Joy
	s3.make_partnership(s0)
	print(f"After Riley dumps Joy and gets back with Jason:\n {s1}, {s3}, {s0}")
	assert not s1.has_partner(), "Remove partnership not working"
	
	s0_rating = s0.get_rating_of_current_partner()
	print(f"{s0}'s rating of current partner", s0_rating)
	assert s0_rating == 2, "Jason should rank their current partner Riley as 2"
	

	# #------------------------------------------------------


	# # new instance of the Group class.  
	student_names_a = ["Anna","Avery","Alastair","Amelia","Abby"]
	student_names_b = ["Bailey","Brian","Beverly","Bob","Biyu"]
	student_group = Group(student_names_a, student_names_b)

	# # Note that these are from least-to-most prefered partner
	# # So Amelia prefers Biyu the most, and Bailiy the least
	student_group.set_ratings({
		'Anna': ['Bob','Brian','Bailey','Beverly','Biyu'],
		'Amelia': ['Bailey', 'Brian', 'Beverly', 'Bob', 'Biyu'],
		'Avery': ['Bailey', 'Biyu', 'Beverly', 'Bob', 'Brian'],
		'Abby': ['Bob', 'Bailey', 'Beverly', 'Biyu', 'Brian'],
		'Alastair': ['Biyu', 'Bob', 'Beverly', 'Bailey', 'Brian'],
		'Biyu': ['Amelia', 'Abby', 'Avery', 'Anna', 'Alastair'],
		'Bailey': ['Anna', 'Avery', 'Alastair', 'Amelia', 'Abby'],
		'Beverly': ['Avery', 'Alastair', 'Amelia', 'Abby', 'Anna'],
		'Bob': ['Amelia', 'Alastair', 'Abby', 'Anna', 'Avery'],
		'Brian': ['Avery', 'Anna', 'Amelia', 'Abby', 'Alastair']
	})


	
	# # Print debug informtation from students
	student_group.print_student_information()
	student_group.print_partnership_quality()

	

	# # Test Task 7
	
	# # Make the naive partnerships
	student_group.make_naive_partnerships()

	# # Print out how satisfied everyone is
	student_group.print_partnership_quality()

	# # Test Task 8 and 9
	print("-"*40 + "\nTest 'make_gale_shapely_partnerships' \n")
	
	# # Now try making pairs with the Gale Shapeley algorithm

	student_group.break_all_partnerships()
	anna = student_group.students_a[0]
	amelia = student_group.students_a[3]
	anna.to_propose = anna.partner_ratings[:]
	amelia.to_propose = amelia.partner_ratings[:]


	# # Biyu should accept Amelia, because Biyu doesn't have a partner yet
	amelia.propose_to_top_choice()
	student_group.print_student_information()
	
	# # Biyu should switch to Anna, dumping Amelia
	anna.propose_to_top_choice()
	student_group.print_student_information()
	
	# # Make Gale-Shapeley pairings
	student_group.make_gale_shapely_partnerships()
	
	# # Print out how satisfied everyone is
	student_group.print_partnership_quality()

	# #------------------------------------------------------
	# # Task 10: Run an experiment
	# # How long does Gale Shapeley take to run?
	# # How happy is everyone?

	print("-"*50 + "\nRunning experiments")

	# # Use this to easily print the results of any test
	def print_test_result(result):
		print(f"Experiment with {result['student_count']} students for {result['run_count']} runs ({result['matchmaking_fxn']})")
		print(f"\tA happiness:       {result['a']:.2f}")
		print(f"\tB happiness:       {result['b']:.2f}")
		print(f"\tAverage happiness: {result['all']:.2f}")
		print(f"\tUnfairness:        {result['unfairness']:.2f} (1 is perfectly fair)")
		print(f"\tTime per run: {result['time']:.4f} milliseconds")


	run_count = 100
	student_count = 100
	fxn_name = "make_gale_shapely_partnerships"
	fxn_name = "make_naive_partnerships"
	
	result = run_experiment(
		student_count=student_count, 
		run_count=run_count, 
		matchmaking_fxn=fxn_name
		)
	print_test_result(result)



	print("\nTest run speed")
	for i in range(1,30):
		run_count = 10
		student_count = 10*i 
		result = run_experiment(
			student_count=student_count, 
			run_count=run_count, 
			matchmaking_fxn="make_gale_shapely_partnerships",
			
		)
		avg_time = result['time']
		time_per_student = avg_time/student_count
		bar = "▇"*round(avg_time*.2)
		print(f"{student_count:10}: {time_per_student:.4f} ms/student {bar}")



	# # A few asserts to verify that Naive is unsatisfying but fair


	
	naive_result = run_experiment(
		student_count=20, 
		run_count=100, 
		matchmaking_fxn="make_naive_partnerships"
		)

	print_test_result(naive_result)
	
	assert math.isclose(naive_result["unfairness"], 1, abs_tol = 0.05) , "We expect GS algorithm to be biased in favor of group A"
	assert math.isclose(naive_result["all"], .5, abs_tol = 0.05) , "We expect an average of about .5 happiness for this size group"

	gs_result = run_experiment(
		student_count=20, 
		run_count=100, 
		matchmaking_fxn="make_gale_shapely_partnerships"
		)
	print_test_result(gs_result)
	
	assert gs_result["a"] > gs_result["b"], "We expect GS algorithm to be biased in favor of group A"
	assert math.isclose(gs_result["all"], .812, abs_tol = 0.05), "We expect an average of about .812 for this size group"
