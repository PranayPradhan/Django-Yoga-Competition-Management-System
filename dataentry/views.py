from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from .models import ScoreIndividual
from participant.models import Participant


def index(request):
    return render(request, "dataentry/index.html")


@require_http_methods(["GET", "POST"])
def bib_verify(request, entry_type):

    if request.method == "POST":
        bib_no_raw = request.POST.get("bib_no")

        try:
            bib_no = int(bib_no_raw)
        except (TypeError, ValueError):
            messages.error(request, "Bib number must be numeric")
            return redirect(request.path)

        if not Participant.objects.filter(bib_no=bib_no).exists():
            messages.error(request, "Bib number not found")
            return redirect(request.path)

        request.session["bib_no"] = bib_no
        request.session["entry_type"] = entry_type

        return redirect("dataentry:score")

    return render(request, "dataentry/bib_verify.html", {
        "entry_type": entry_type
    })


@require_http_methods(["GET", "POST"])
def score_entry(request):

    bib_no = request.session.get("bib_no")
    entry_type = request.session.get("entry_type")

    if bib_no is None or entry_type is None:
        return redirect("dataentry:index")

    try:
        bib_no = int(bib_no)
    except (TypeError, ValueError):
        return redirect("dataentry:index")

    score_obj = ScoreIndividual.objects.filter(bib_no=bib_no).first()

    if score_obj is None:
        messages.error(request, "Score record not found")
        return redirect("dataentry:index")

    # 🔒 HARD NORMALIZATION (THIS FIXES THE ERROR)
    if entry_type == "yoga":
        current_score = score_obj.value
    else:
        current_score = score_obj.coc_value

    if current_score is None:
        current_score = Decimal("0.00")

    # Convert to string explicitly (critical)
    current_score = str(current_score)

    if request.method == "POST":

        if "cancel" in request.POST:
            return redirect("dataentry:index")

        raw_score = request.POST.get("score", "").strip()

        try:
            score = Decimal(raw_score)
        except (InvalidOperation, TypeError):
            messages.error(request, "Score must be a number")
            return redirect("dataentry:score")

        if score < 0:
            messages.error(request, "Score cannot be negative")
            return redirect("dataentry:score")

        if entry_type == "yoga":
            score_obj.value = score
        else:
            score_obj.coc_value = score

        score_obj.save()

        messages.success(request, "Score saved successfully")

        return redirect("dataentry:index")

    return render(request, "dataentry/score_entry.html", {
        "bib_no": bib_no,
        "score": current_score,
        "entry_type": entry_type,
    })
