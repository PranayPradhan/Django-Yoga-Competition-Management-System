from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum, OuterRef, Subquery, Max
from masters.models import Gender, YogaSubCat, AgeCategory
from participant.models import Participant
from dataentry.models import ScoreIndividual

# Create your views here.

def index(request):
    # get all yoga sub categories
    yoga_sub_cats = YogaSubCat.objects.all()

    # return HttpResponse("Reached report app index")   
    return render(request, "report/index.html", {
                  "title": "Report Index Page",
                  "yoga_sub_cats": yoga_sub_cats
                  })


def competition_results(request):

    # line_break = "<br>" # - line break to send HTTP response directly to browser
    line_break = "\n" # - line break for writing in the text file

    # fetching yoga sub categories from m_yoga_sub_cat table
    yoga_sub_categorys = YogaSubCat.objects.all()
    # yoga_sub_categorys = YogaSubCat.objects.get(name="Traditional")

    # fetch age categories from m_age_cat table
    age_cats = AgeCategory.objects.all()
    # age_cats = AgeCategory.objects.get(name="U11")

    # fetch genders from m_gender table
    genders = Gender.objects.all()
    # genders = Gender.objects.get(name="Boys")

    # function to generate yoga sub category result
    def generate_yoga_sub_category_result():
        # ------------------------ Yoga Sub Category Result ------------------------
        content = ""
        content += f"Yoga Sub Category Result{line_break}"
        content += f"===================================================={line_break}{line_break}"

        # iterate through yoga sub categories,
        for yoga_sub_cat in yoga_sub_categorys:

            content += f"Yoga Sub Category: {yoga_sub_cat.name}{line_break}"
            content += f"===================================================={line_break}"

            # iterate through age categories
            for age_cat in age_cats:


                # iterate through genders
                for gender in genders:
                    # add score of all individual participants of a school to total_score
                    # arrange in desc order to get the school with the highest total_score
                    # TODO: check for joint winners
                    # Joint winners can be handled later with filter(total_score=winner["total_score"])

                    school_code_sq = Participant.objects.filter(
                        bib_no=OuterRef("bib_no")
                        ).values("school__code")[:1]

                    winner = (
                        ScoreIndividual.objects
                        .filter(
                            yoga_sub_cat_id=yoga_sub_cat.pk,
                            age_cat_id=age_cat.pk,
                            gender_id=gender.pk,
                        )
                        .annotate(school_code=Subquery(school_code_sq))
                        .values("school_code")
                        .annotate(total_score=Sum("value"))
                        .order_by("-total_score")
                        .first()
                    )
                    if winner:
                        school_code = winner["school_code"]
                    
                    # print the list of participants from the winning school
                    content += f"Yoga Sub Category: {yoga_sub_cat.name}{line_break}"
                    content += f"Category: {age_cat.name} {gender.name}{line_break}"
                    content += f"Winner: {school_code}{line_break}"     
                    content += f"Winning Team Members:{line_break}"
                    content += f"-------------------------------{line_break}"
                    content += f"SN\t\tBib No.\t\tName{line_break}"
                    content += f"-------------------------------{line_break}"

                    # get name of all the participants of the winner school
                    rows = (
                        Participant.objects
                        .filter(
                            age_cat_id=age_cat.pk,
                            yoga_sub_cat_id=yoga_sub_cat.pk,
                            gender_id=gender.pk,
                            school__code=school_code,
                        )
                        .values("bib_no", "name")
                    )
                                    
                    sn = 1 # for serial number of items being displayed
                    if rows:
                        for row in rows:
                            content += f"{sn}\t\t{row["bib_no"]}\t\t{row["name"]}{line_break}"
                            sn += 1    
                    else:
                        content += f"*** No Participants ***{line_break}"

                    content += f"{line_break}"

            content += f"{line_break}{line_break}"

        return content

    # function to generate champion of champions result
    def generate_champion_of_champions_result():
        # ------------------------ Champion of Champions Result ------------------------
        content = ""
        content += f"Champion of Champions Result{line_break}"
        content += f"============================================================================{line_break}"
        content += f"Sn\tAge Cat\tGender\tBib No.\tName\t\tSchool Code{line_break}"
        content += f"----------------------------------------------------------------------------{line_break}"

        # get coc winners from score_individual table
        # select highest coc_value score from gender

        # # get gender into a dictionary for iteration and mapping
        genders = Gender.objects.all()

        if genders:
            sn = 1
            for gender in genders:
                gender_id = gender.pk
                gender = gender.name                

                # get the max coc score for each gender  
                rows = (
                    ScoreIndividual.objects
                    .filter(
                        gender_id=gender_id,
                        is_coc=True
                    )
                    .values("gender_id")
                    .annotate(max_coc_value=Max("coc_value"))
                )
                if rows:
                    for row in rows:
                        max_coc_value = row["max_coc_value"]
                        # content += f"{max_coc_value}{line_break}"

                        # get all coc winners with max coc value by gender
                        # as there is a possibility of multiple coc winners with same score
                        if(max_coc_value > 0): # if there are participants for coc

                            participants = Participant.objects.filter(
                                bib_no=OuterRef("bib_no")
                            )

                            coc_winners = (
                                ScoreIndividual.objects
                                .filter(
                                    gender_id=gender_id,
                                    is_coc=True,
                                    coc_value=max_coc_value
                                )
                               .annotate(
                                    participant_name=Subquery(participants.values("name")[:1]),
                                    school_name=Subquery(participants.values("school__name")[:1]),
                                )
                                .values(
                                    "age_cat",
                                    "gender",
                                    "bib_no",
                                    "participant_name",
                                    "school_name",
                                )
                            )

                            if coc_winners:
                                for coc_winner in coc_winners:
                                    # content += f"{coc_winner}{line_break}"
                                    content += f"{sn}\t{coc_winner["age_cat"]}\t{coc_winner["gender"]}\t{coc_winner["bib_no"]}\t {coc_winner["participant_name"]}\t\t{coc_winner["school_name"]}{line_break}"
                                    sn += 1
                        else:
                            content += f"*** No Champion of Champions Winner for Gender: {gender} ***{line_break}"
                
            content += f"{line_break}{line_break}"

        return content

    def school_championship_result():
        # ------------------------ School Championship Result ------------------------
        content = ""
        content += f"School Championship Result{line_break}"
        content += f"============================================================================{line_break}"
        content += f"Rank\tTotal Score\t\tSchool Name{line_break}"
        content += f"----------------------------------------------------------------------------{line_break}"    

        # get "total score" for each "school" which is the sum of all individual scores of 
        # participants from that school     
        scores = (
            ScoreIndividual.objects
            .filter(bib_no=OuterRef("bib_no"))
            .values("bib_no")
            .annotate(total=Sum("value"))
            .values("total")
        )

        # get top 3 rows of school arranged by descending order of total score
        rows = (
            Participant.objects
            .annotate(total_score=Subquery(scores))
            .values("school__name")
            .annotate(total_score=Sum("total_score"))
            .order_by("-total_score")[:3]
        )

        # print top 3 schools acording to total score and ranked from 1 to 3
        if rows:
            sn = 1
            for row in rows:
                # content += f"{row}{line_break}"

                content += f"{sn}\t\t{row["total_score"]}\t\t{row["school__name"]}{line_break}"
                sn += 1
        else:
            content += f"*** No Schools Championship Result Available ***{line_break}"

        return content

    # call individual fuctions to generate parts of the total competition result
    content = generate_yoga_sub_category_result()
    content +=  generate_champion_of_champions_result()
    content +=  school_championship_result()

    content += f"{line_break}{line_break}"
     
    # Create the HttpResponse object for the text file
    filename = f"competition_results.txt"
    response = HttpResponse(
        content_type="text/plain",
        # headers={"Content-Disposition": 'attachment; filename= ' + filename + ''},
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
    
    response.write(content)

    return response    
    # return HttpResponse(content)  # - for viewing directly on browser during development



# function to generate Champion of Champions call sheet
def coc_mc_call_sheet(request):
    content = ""
    # TODO: The hardcoded "Traditional" should be controlled from settings table later
    allowed_yoga_sub_cat = "Traditional"
    # get the yoga sub category pk for the allowed yoga sub category
    yoga_sub_cat = YogaSubCat.objects.get(name=allowed_yoga_sub_cat)


    # TODO: U11 Age Category participants are not allowed to partiticipat in COC. Should be controlled by setting table later
    restricted_age_cat = "U11"
    # Get traditional yoga sub category id from master table
    # Champion of Champions is selected only from Traditional Yoga Sub Category

    # get the age categories for the allowed age category only
    age_cats = AgeCategory.objects.filter().exclude(name__in=[restricted_age_cat])

    # get the gender records
    genders = Gender.objects.all()

    # line_break = "<br>" # - line break to send HTTP response directly to browser
    line_break = "\n" # - line break for writing in the text file

    # Clear coc winners bib number score_individual table
    # set is_coc_winner to FALSE for ALL bib_no first to clear previous winners
    ScoreIndividual.objects.update(is_coc=False)

    # prepare Champion of Champions call sheet content
    # global content
    content += f"MC Call Sheet - Champion of Champions - QUALIFIED PARTICIPANTS{line_break}"
    content += f"=============================================================={line_break}{line_break}"

    # iterate through genders
    for gender in genders:
        content += f"{gender} - QUALIFIED FOR - Champion of Champions{line_break}"
        content += f"====================================================={line_break}"
        content += f"SN\t\tCategory\t\tBib No:\t\tScore{line_break}"
        content += f"-----------------------------------------{line_break}"

        # iterate through age categories
        sn = 1 # to serial number the winners of each age category
        for age_cat in age_cats:

            # prepare query
            q = ScoreIndividual.objects.filter(
                yoga_sub_cat_id=yoga_sub_cat.pk,
                age_cat__name=age_cat,
                gender__name=gender,
            ).order_by("-value")

            # execute query. In this case, select the first row only.
            # TODO: logic for joint winners
            row = q.first()

            if row:
                # extract fields
                bib_no = row.bib_no
                score = row.value

                content += f"{sn}\t\t{age_cat} - {gender}\t\t{bib_no}\t\t\t{score}{line_break}"
                # content += f"{sn}\t\t{age_cat} - {gender}{line_break}"
                sn += 1

                # set ONLY is_coc to TRUE for the coc winners
                ScoreIndividual.objects.filter(bib_no=bib_no).update(is_coc=True)
                
            else:
                content += f" **** No Participant qualified ****{line_break}"
                # content 

        content += f"{line_break}{line_break}"
     
    # Create the HttpResponse object for the text file
    filename = f"coc_mc_call_sheet.txt"
    response = HttpResponse(
        content_type="text/plain",
        # headers={"Content-Disposition": 'attachment; filename= ' + filename + ''},
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
    
    response.write(content)

    return response    
    # return HttpResponse(content)  # - for viewing directly on browser during development

def event_mc_call_sheet(request, pk):
   
    # get one yoga sub category as selected by user
    yoga_sub_cat = YogaSubCat.objects.get(pk=pk)

    # get all age categories and gender record
    age_cats = AgeCategory.objects.all()
    genders = Gender.objects.all()

    # line_break = "<br>" # - line break to send HTTP response directly to browser
    line_break = "\n" # - line break for writing in the text file

    # for the selected yoga sub category, prepare the call sheet report
    content = ""
    content += f"MC Call Sheet - Yoga Sub Category: {yoga_sub_cat.name}{line_break}"
    content += f"===================================================={line_break}"
    content += f"{line_break}"

    # iterate through age categories
    for age_cat in age_cats:

        # iterate through genders
        for gender in genders:
            content += f"Age Category: {age_cat.name} {gender.name}{line_break}"
            content += f"===================================================={line_break}"
            content += f"Bib No:{line_break}"
            content += f"-------{line_break}"

            # get all the bib number of participants of this yoga cat, age cat & gender
            bib_nos = (
                Participant.objects
                .filter(
                    yoga_sub_cat_id=yoga_sub_cat.pk,
                    age_cat_id=age_cat.pk,
                    gender_id=gender.pk,
                )
                .order_by("bib_no")
                .values_list("bib_no", flat=True)
            )

            # check if there are participants for the given criteria
            if bib_nos:
                for bib_no in bib_nos:
                    content += f"{bib_no}{line_break}"
            else:
                content += f"***** No Participant *****{line_break}"

            content += line_break

    # Create the HttpResponse object for the text file
    filename = f"event_mc_call_sheet_{yoga_sub_cat.name}.txt"
    response = HttpResponse(
        content_type="text/plain",
        # headers={"Content-Disposition": 'attachment; filename= ' + filename + ''},
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
    
    response.write(content)

    return response    
    # return HttpResponse(content)  # - for viewing directly on browser during development