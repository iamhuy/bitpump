from django.core.management.base import BaseCommand
from activity.models import *
from app_user.models import *
import math
import time

similar_weight = {
    'Age': 10,
    'Gender': 1,
    'Team': 1,
    'History': 100,
    'tech': 1,
    'sports': 1,
    'hobby': 1
}
sum_weight = sum(similar_weight.values())

activities = {
    'Sports': [

    ],
    'English Talk': [

    ],
    'Hangout': [

    ],
    'Sharing': [

    ]

}


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('poll_ids', nargs='+', type=int)

    def age_point(self, age1, age2):
        t = abs(age1-age2)
        if t < 3:
            return 0
        elif t < 5:
            return 0.3
        elif t < 10:
            return 0.7
        else:
            return 1

    def gender_point(self, gender1, gender2):
        if gender1 == gender2:
            return 1
        return 0

    def team_psoint(self, team1, team2):
        if team1 == team2:
            return 1
        return 0

    def similar_cal(self, user1, user2):
        diff_vec = []

        attr1 = {}
        attr2 = {}
        for x in UserAttribute.objects.filter(user__id=user1.id).alls():
            attr1[x.name] = x.value
        for x in UserAttribute.objects.filter(user__id=user2.id).alls():
            attr2[x.name] = x.value

        activities = set(UserActivity.objects.fitler(user__id=user1.id).values_list('activity__id', flat=True)) & (
            UserActivity.objects.fitler(user__id=user1.id).values_list('activity__id', flat=True))
        if len(activities) > 0:
            diff_vec.append(similar_weight['History']/sum_weight)

        diff_vec.append(similar_weight['Age'] / sum_weight * self.age_point(attr1['Age'], attr2['Age']))

        diff_vec.append(similar_weight['Gender'] / sum_weight * self.gender_point(attr1['Gender'], attr2['Gender']))

        diff_vec.append(similar_weight['Team'] / sum_weight * self.team_point(attr1['Team'], attr2['Team']))

        similarity = math.sqrt(sum([x*x for x in diff_vec]))

        return similarity

    def points_cal(self, users):
        points = {}
        for user1 in users:
            points[user1] = {}
            for user2 in users:
                points[user1][user2] = -1

        for user1 in users:
            for user2 in users:
                if user2 == user1:
                    continue
                if points[user2][user1] != -1:
                    points[user1][user2] = points[user2][user1]
                    continue
                points[user1][user2] = self.similar_cal(user1, user2)

        return points

    def match_draws(self, category, draws):
        users = []
        user_to_draw = {}
        for draw in draws:
            users.append(draw.user)
            user_to_draw[draw.user] = draw

        points = self.points_cal(users)

        while len(users) >= 2:
            optimal_pair = (None, None)
            for user1 in users:
                for user2 in users:
                    if points[user1][user2] != -1:
                        if optimal_pair[0] is None:
                            optimal_pair = (user1, user2)
                            continue
                        if points[user1][user2] < points[optimal_pair[0]][optimal_pair[1]]:
                            optimal_pair = (user1, user2)

            user1, user2 = optimal_pair
            draw_user_1, draw_user_2 = user_to_draw[user1], user_to_draw[user2]
            users.remove(user1)
            users.remove(user2)
            draw_user_1.status = UserLuckyDraw.STATUS_MATCHED
            draw_user_1.save()
            draw_user_2.status = UserLuckyDraw.STATUS_MATCHED
            draw_user_2.save()

            Activity.objects.create(
                activity_category=category,
                longtitude=0,
                latitude=0,
                place_name='',
                time=time.time(),
                status=Activity.STATUS_INIT
            )

    def handle(self, *args, **options):
        cur_draws = UserLuckyDraw.objects.filter(status=UserLuckyDraw.STATUS_INIT).all()
        category_to_draws = {}
        for draw in cur_draws:
            category_to_draws.setdefault(draw.activity_category, []).append(draw)
        for category, draws in category_to_draws.iteritems():
            self.match_draws(category, draws)
