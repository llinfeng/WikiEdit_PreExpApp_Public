# Update by Linfeng
The games in this repo does not work with newer version of oTree out of the box,
mostly due to the `Competitiveness` game, introduce through the `jbef-channels`
repo.

Here is the plan to adopt it for production
1. First, we have minimum app where addition tasks are generated, and
2. Second, we schedule the three rounds where: 
    * Round 1 is piece rate,
    * Round 2 is tournament with 3 others (only know if outperformed or not, but
      not the full distribution for sure)
    * Round 3 is up to the subject to choose

The original game with adding a random set of numbers is from Repo:
[otree-tools/jbef-channels: a repository containing the code for the paper 'Real
time interactions in oTree using Django Channels: auctions and real effort
tasks'](https://github.com/otree-tools/jbef-channels#niederle2007)


For other games that are forked into this repo, See the [Source of apps](#Source
of apps) section below.
----

# Notes for calculating payoff:
Students do not see their total points at the end of the experiment. Whenever
necessary, the will see the payoff for each round.
1. Holt & Laury with curiosity: payoff is revealed, but not necesarily the
   lottery chosen for payment;
2. Trust respondre - Strateg method - revealed payment upon finishing
3. Trust investor - paired with a randomly drawn opponent, payoff revealed upon
   finishing;
4. p-Beauty contest: over 5 rounds, 1 round is chosen for payment. There is a
   payment page at the end of all 5 arouds.

# Dev notes

## Caveats:

### Caveat 1 - Games are scheduled in fixed order if launched in one session.
For apps hosted in a session, the app sequence is fixed
* Comment 1, from the forum, confirming that app-sequence is fixed: [Randomization of app sequence per player or group](https://groups.google.com/g/otree/c/JHP91_ZpGos/m/tj1UhOSGAAAJ)
* Discussion 2: `app_after_this_page` may be helpful, but not necessarily - [New
  beta feature: skipping many pages or apps](https://groups.google.com/g/otree/c/T6DsbOv712Q/m/Qq_Tv8ZBAgAJ)

* [ ] There is a way to solve this, to span out all combination of the app
      sequences and send them out!


## Style of the games
`custom.css` is reused heavily. Originally, this file is from `mpl`. Hosting
with refernces to `mpl` created problem with Heroku.
```
{% block styles %}
    <link href="{% static 'global/custom.css' %}" rel="stylesheet"/>
{% endblock %}

    <div class="wrapper instructions">
    Then, the formal intro and instrucitons.
    </div>
```
This CSS sheet is reused heavily throughout this deck of oTree apps.


## Source of apps
We list the name of the app (dir name) and where we get them, as the start.
1. Holt & Laury: `mpl`, from <https://www.otreehub.com/projects/cl-demo/>, by
   Felix Holzmeister 
    * [ ] Add willingness to pay for revealing the lottery of choice
    * [ ] Prevent multiple-crossing should it occur, and ask subject to redo
2. Trust - investor: `trust_investor`, from `otree_demo`
    1. Tokenized: that there are 5 tokens, each worths 20 points
    2. Converted so that payoff is realized with random-matching with a
       historical play (based on strategy method)
3. Trust - responder: `trust_responder`, from `otree_demo`  
    1. 6 rounds, strategy method, where 0-5 tokens were sent each round.
4. p-Beauty contest: `guess_two_thirds`, from `otree_demo`
5. Pending - Competitiveness: pending - not sure if the task sufficies
   <https://github.com/otree-tools/jbef-channels#niederle2007>, the demo works
   remotely, and should need `otree==2.5.8` (older oTree)
    * [x] Runs locally with `oo_create`, a Zsh function
    * [x] Need Python Runtime to be `python-3.7.4`, in the `runtime.txt` file when
      pubhsed to Heroku
    * Now the thing runs on Heroku, with an added Redis database
6. Pending - Knapsack: 
    * Source: [JavaScript table without retry](https://www.otreehub.com/projects/pack-your-backpack/)
    * JavaScript pulls from the `App/data` folder, for `parts_1.csv` ... as the
      raw list of items in the backpack
    * A folder-full of Javascript files needs to go to
      `/App/_static/java_script/`, with:
    ```
    compute_weight.js
    create_decision_table.js
    create_result_table.js
    save_selection.js
    table_sort.js
    ```


# Summary of apps
Before the main treatment, we were using a battery of MobLab games to collect:
1. Informed consent (first page as people join the experiment);
2. Gender of the participant (for stratified random assignment);
3. A battery of games

## Informed consent
* [ ] Construct a HTML view of the `Informed_Consent_IRB_Full_2019_0307.docx`
      This file was shared with MobLab and was pushed to the registration page.

## Survey
* [ ] Convert to a survey app: need proofreading.
      Source: [Pure text in word format of the survey is available here.](~/Dropbox/2018_Wikipedia_Women/IRB/IRB_Q29_Survey/Survey_Template.md)

## Games
1. Holt & Laury
2. Trust - investor
3. Trust - responder
4. p-Beauty contest
5. Competitiveness: round 1, round 2 and round 3.
6. Knapsack: the game should not be as grinding as the MobLab version
    * The game features:
        1. All packages are displayed in a table,
        2. Columns in the table can be sorted
        3. If capacity is reached, there will be a live warning.
    * Source: [JavaScript table without retry](https://www.otreehub.com/projects/pack-your-backpack/)
    * TODO:
        * [ ] Update the table so that we use the same set of games


# Whereabouts of games and how to convert them
1. Consent page: first thing before any other compartment
2. Get all the games ready: 
    * [ ] add bots to games - trust + p-Beauty, along with bot strategies
    List of games and where to find them + pull emperical choices from previous round.
    1. Holt & Laury: [mpl from this oTree package](https://www.otreehub.com/projects/cl-demo/)
        * oTree >= 2.2.4
        * Parameters: 10 pairs of lotteries - (5,4) vs (10, 1), with varying
          probabilities in (1/10, 9/10) ... (1, 0)
        * [ ] On tuning the game: use `config.py` in the folder
            * `enforce_consistency` is implemented without warning: subsequent
              radio buttons are populated automatically.
            * Curiosity: we will show the payoff from the lottery first, at the
              top of the page. The rest of the page has a slider to choose the
              WTP.
                * In th result page, the chosen lottery is reported if the
                  conitoins are satisfied.
        
    2. Trust - investor: adopt from [demo-trust](https://github.com/oTree-org/otree)
    3. Trust - responder: adopt from [demo-investor](https://github.com/oTree-org/otree)
    4. p-Beauty contest: adop from [demo-guess_two_thirds](https://github.com/oTree-org/otree)
    5. Competitiveness: round 1, round 2 and round 3.
        1. [Paper with oTree? Willing to share the code?](https://www.sciencedirect.com/science/article/abs/pii/S016726811830310X?via%3Dihub
            1. David Klinowski - [David Klinowski](https://davs-econ.github.io/)
        2. [otree-tools/jbef-channels: a repository containing the code for the paper 'Real time interactions in oTree using Django Channels: auctions and real effort tasks'](https://github.com/otree-tools/jbef-channels#niederle2007)
    6. Knapsack: the game should not be as grinding as the MobLab version
        * The game features:
            1. All packages are displayed in a table,
            2. Columns in the table can be sorted
            3. If capacity is reached, there will be a warnig.
        * Source: [JavaScript table without retry](https://www.otreehub.com/projects/pack-your-backpack/)
            * oTree >= 2.2.4
3. Arrange with prespecified orders
    * [ ] Search oTree forum: games with randomized orders



# Archive

Tihs repo is adoped from the `realefforttask` repo, where these are the original
documentations:

## Real time interactions in oTree using Django Channels
### Auctions and real effort tasks
This code contains four applications to use in oTree [Chen2016]_.

The demo app based on this code is available at Heroku_.


1. :code:`minimum`: a bare  example how to use Django Channels in oTree projects
to build a very simple real effort task (subtracting random number from X).


2. :code:`realefforttask`: a set of four different real effort tasks:

-  summing up *N* numbers [Niederle2007]_.
- finding max of two matrices [Schram2017]_.
- decoding task [Erkal2011]_.
- counting 0s in a matrix [Abeler2011]_.

This app also provides a platform for development one's own tasks using
TaskGenerator class from :code:`ret_functions` module located in :code:`realefforttask` app folder.
To use it, create a child of :code:`TaskGenerator` class in :code:`ret_functions` module, and reference it
in :code:`settings.py` configuration for your app.


3. :code:`auctionone` -  a gift-exchange game [Fehr1993]_ where employers hire workers in the
open auction, and workers reciprocate their salary in a subsequent real effort task stage.

4. :code:`double_auction` -  a trading platform where buyers and sellers can
trade their goods by posting bids (for buyers) and asks (for sellers) [Smith1962]_.



### References
--------
.. _Heroku: https://jbef-channels.herokuapp.com/
.. [Chen2016] Chen, D. L., Schonger, M., & Wickens, C. (2016). oTree—An open-source platform for laboratory, online, and field experiments. Journal of Behavioral and Experimental Finance, 9, 88-97.
.. [Niederle2007] Niederle, M., & Vesterlund, L. (2007). Do women shy away from competition? Do men compete too much?. The quarterly journal of economics, 122(3), 1067-1101.
.. [Schram2017] Weber, M., & Schram, A. (2017). The Non‐equivalence of Labour Market Taxes: A Real‐effort Experiment. The Economic Journal, 127(604), 2187-2215.
.. [Erkal2011] Erkal, N., Gangadharan, L., & Nikiforakis, N. (2011). Relative earnings and giving in a real-effort experiment. American Economic Review, 101(7), 3330-48.
.. [Abeler2011] Abeler, J., Falk, A., Goette, L., & Huffman, D. (2011). Reference points and effort provision. American Economic Review, 101(2), 470-92.
.. [Fehr1993] Fehr, E., Kirchsteiger, G., & Riedl, A. (1993). Does fairness prevent market clearing? An experimental investigation. The quarterly journal of economics, 108(2), 437-459.
.. [Smith1962] Smith, V. L. (1962). An experimental study of competitive market behavior. Journal of political economy, 70(2), 111-137.

