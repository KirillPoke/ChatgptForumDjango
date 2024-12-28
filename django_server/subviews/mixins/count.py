from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Case, When, IntegerField


class ScoreCountMixin:
    score_type = ""

    @action(detail=False, methods=["get"], url_path="count")
    def count_scores(self, request):
        ids = request.query_params.get(f"{self.score_type}_ids", "").split(",")

        if not ids or not ids[0]:
            return Response({"error": "ids required"}, status=400)

        try:
            ids = [int(id) for id in ids]
        except ValueError:
            return Response({"error": "invalid ids format"}, status=400)

        filter_kwargs = {f"{self.score_type}_id__in": ids}
        scores = {
            score[f"{self.score_type}_id"]: {
                f"{self.score_type}_id": score[f"{self.score_type}_id"],
                "upvotes": score["upvotes"],
                "downvotes": score["downvotes"],
                "total_score": score["upvotes"] - score["downvotes"],
            }
            for score in self.get_queryset()
            .filter(**filter_kwargs)
            .values(f"{self.score_type}_id")
            .annotate(
                upvotes=Count(
                    Case(When(upvote=True, then=1), output_field=IntegerField())
                ),
                downvotes=Count(
                    Case(When(upvote=False, then=1), output_field=IntegerField())
                ),
            )
        }

        return Response(
            [
                scores.get(
                    score_fk_id,
                    {"id": score_fk_id, "upvotes": 0, "downvotes": 0, "total_score": 0},
                )
                for score_fk_id in ids
            ]
        )


class PostScoreCountMixin(ScoreCountMixin):
    score_type = "post"


class CommentScoreCountMixin(ScoreCountMixin):
    score_type = "comment"
