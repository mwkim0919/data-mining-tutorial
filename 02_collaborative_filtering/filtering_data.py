import argparse
import colorama
from math import *
from tabulate import tabulate

colorama.init(autoreset=True)

users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
         "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5, "Slightly Stoopid": 1.0},
         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},
         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0, "Vampire Weekend": 1.0},
         "Jordyn":  {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0},
         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0, "Slightly Stoopid": 4.0, "The Strokes": 5.0},
         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5, "The Strokes": 3.0}
        }


def printDataSet(users: dict) -> None:
  headers = ['Users', 'Blues Traveler', 'Broken Bells', 'Deadmau5', 'Norah Jones',
            'Phoenix', 'Slightly Stoopid', 'The Strokes', 'Vampire Weekend']
  # minifiedHeaders = ['Users', 'B.T.', 'B.B.', 'Deadmau5', 'N.J.',
  #                   'Phoenix', 'S.S.', 'The Strokes', 'V.W.']
  userRatings = []
  for user in users.keys():
    rating = []
    rating.append(user)
    for index in range(1, len(headers)):
      if headers[index] in users[user]:
        rating.append(users[user][headers[index]])
      else:
        rating.append(None)
    userRatings.append(rating)
  print(tabulate(userRatings, headers))


def manhattan(user1: dict, user2: dict) -> float:
  """
  Compute the Manhattan distance. (difference in x and y)
  :return: Manhattan distance
  """
  distance = 0
  for artist in user1:
    if artist in user2:
      distance += abs(user1[artist] - user2[artist])
  return distance


def pearson(rating1: dict, rating2: dict) -> float:
  """
  Compute Pearson Correlation Coefficient.
  (Reducing variability. e.g. Does Hailey's 4 mean the same as Jordyn's 4?)
  :return: Pearson Correlation Coefficient
  """
  sum_xy = sum_x = sum_y = sum_x2 = sum_y2 = n = 0
  for artist in rating1:
    if artist in rating2:
      n += 1
      x = rating1[artist]
      y = rating2[artist]
      sum_xy += x * y
      sum_x += x
      sum_y += y
      sum_x2 += x**2
      sum_y2 += y**2

  if n == 0:
    return 0
  
  denominator = sqrt(sum_x2 - (sum_x**2) / n) * sqrt(sum_y2 - (sum_y**2) / n)
  if denominator == 0:
    return 0
  else:
    return (sum_xy - (sum_x * sum_y) / n) / denominator


def minkowski(user1: dict, user2: dict, r: float) -> float:
  """
  Compute the Minkowski distance.
  :return: Minkowski distance
  """
  distance = 0
  commonRating = False
  for artist in user1:
    if artist in user2:
      distance += pow(abs(user1[artist] - user2[artist]), r)
      commonRating = True
  if commonRating:
    return pow(distance, 1/r)
  else:
    return 0.0


def computeNearestNeighbor(username: str, users: dict, exponent: int) -> list:
  """
  Create a sorted list of users based on their distance to username
  :return: list of users with similar preference
  """
  distances = []
  for user in users:
    if user != username:
      distance = minkowski(users[user], users[username], exponent)
      distances.append((distance, user))
  distances.sort()
  return distances


def recommend(username: str, users: dict, exponent: int) -> list:
  """
  Give list of recommendations.
  :return: list of artist recommendation
  """
  nearest = computeNearestNeighbor(username, users, exponent)[0][1]
  recommendations = []
  neighborRatings = users[nearest]
  userRatings = users[username]
  for artist in neighborRatings:
    if not artist in userRatings:
      recommendations.append((artist, neighborRatings[artist]))
  return sorted(recommendations,
                key=lambda artistTuple: artistTuple[1],
                reverse = True)


def main():
  """Parse arguments."""
  parser = argparse.ArgumentParser()
  parser.add_argument('user',
                    help='Provide one of the user: {' + ' '.join(users.keys()) + '}')
  parser.add_argument('--exponent', '-e', default=1,
                    help='Provide the exponent to be used. (e.g. 1 = Manhattan, 2 = Euclidean)')
  parser.add_argument('--pearson', '-p', action='store_true',
                    help='Just invoke Pearson Correlation. This will need -r1 & -r2.')
  parser.add_argument('--rating1', '-r1', default='',
                    help='Provide one of the user: {' + ' '.join(users.keys()) + '}')
  parser.add_argument('--rating2', '-r2', default='',
                    help='Provide one of the user: {' + ' '.join(users.keys()) + '}')
  args = parser.parse_args()
  printDataSet(users)
  if not args.pearson:
    print(colorama.Fore.YELLOW + args.user + '\'s Artist Recommendation: ')
    print(colorama.Fore.GREEN + str(recommend(args.user, users, float(args.exponent))))
  else:
    print(colorama.Fore.GREEN + str(pearson(users[args.rating1], users[args.rating2])))

if __name__ == '__main__':
  main()

