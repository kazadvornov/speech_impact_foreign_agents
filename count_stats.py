import re
import os.path
from bs4 import BeautifulSoup


strat_full_names = {"l": "putting on labels",
                    "sia": "supposed integration of the speaker to the listening audience",
                    "eud": "emphasizing someone's unworthiness of trust, defaming them",
                    "bvtmi": '''introduction of "bi-value thinking model" ''',
                    "ce": "presenting single deeds as constant situation",
                    "dv": "decriminalizing violence and making the people get used to it and consider it "
                          "an effective instrument for solving the problems",
                    "dilu": "uncovering the mysteries of death and people's intimate life",
                    "ema": "emphasizing the actor",
                    "dea": "deemphasizing the actor",
                    "cfpa": "calling for acting in a particular way",
                    "df": "destruction of the barrier between the beautiful and ugly, pleasant and disgusting, "
                          "diminishing the fastidiousness and innate disgust to the ugly things",
                    "utca": "undermining the authority of religious and other traditions and customs",
                    "piwl": "Creating the pleasant imagination of life in Western countries and exclude the access "
                            "of any information revealing some of its unpleasant sides",
                    "st": '''Replacement of Russian cultural keywords having become a base for derivation of 
                          many other words with the foreign or invented words ("semantic terrorism")''',
                    "dsps": "defaming the state and power symbols",
                    "mc": "choosing a particular modality to describe an event",
                    "qii": "introducing some information without thinking and checking",
                    "bep": "breaking the existing presuppositions",
                    "eip": "emphasizing a part of information",
                    "gco": "changing the addressee's opinion about something through generalization",
                    "soes": "strengthening the overall emotional state of the addressee",
                    "efc": "establishing false connections between the events "
                           "(placing the information in particular way)",
                    "fns": "fixing the needed stereotypes in the consciousness",
                    "emms": "creating negative images through the epithets, metaphors, methonymies and synecdoches",
                    "app": "appealing to the addressee",
                    "rst": "reversed semantic terrorism"}


mean_full_names = {"sads": "Words derived through affixation and stem composition "
                           "where stem(s) and affix(es) belong to different styles",
                   "fsravv": "Words derived from foreign stems with the help of Russian productive affixes",
                   "clua": "Colloquial lexical unit affixes, including petting, augmentative and feminitive suffixes",
                   "egn": "Names of groups, their representatives, attributes and actions with "
                          "bright evaluative components of meaning, either positive or negative",
                   "fppvf": "first-personal pronouns and first-personal plural forms of verbs",
                   "tppvf": "third-personal pronouns and third-personal verb forms",
                   "anth": "anthonyms",
                   "oj": "overgeneralized judgements about represenatives of a group, complicated or "
                         "many-sided phenomena",
                   "wmc": '''using quantifiers like "every", "all", "each", the words with the meaning of constancy, 
                            high frequency  or their lengthiness in time''',
                   "vpt": "the present-time forms of verbs",
                   "dtvf": "the nearby situated different tense forms of verbs",
                   "wvm": "words semantically related to violent actions, pain, suffering and injuries",
                   "wsfi": "the words form the semantic field of illnesses",
                   "wsk": "words with the semantics of death and killing living creatures",
                   "ils": '''words from the semantic field "Sexual relationships", particularly naming genitalies, 
                            sexual act itself, underwear and other things contextually related to the intimate life 
                            sphere''',
                   "avs": "using active verb forms",
                   "pvs": "using passive verb forms",
                   "ops": "one-part sentences with one member-predicate",
                   "pn": "process nominalizations",
                   "uifap": "using imperative verb forms and particles traditionally used in imperative sentences",
                   "cvolu": "colloquial, vulgar and obscene lexical units",
                   "tfrc": "words naming things forbidden in the Russian culture",
                   "lowp": "words naming living organisms' waste products and associated with them",
                   "ssa": '''Words from the semantic field of unpleasant effects on sence organs, 
                            particularly the names of things that taste, smell bad or are unpleasant to touch 
                            ("sensory speech aggression")''',
                   "rn": "word combination(s) in a sentence expressing syntactic connections "
                         "between words connected with religion and those having destructive, demolishing and (or) "
                         "negatively evaluative components of meaning",
                   "tn": "word combination(s) in a sentence expressing syntactic connections "
                         "between words connected with traditions and those having destructive, demolishing and (or) "
                         "negatively evaluative components of meaning",
                   "cn": "word combination(s) in a sentence expressing syntactic connections "
                         "between words connected with customs and those having destructive, demolishing and (or) "
                         "negatively evaluative components of meaning",
                   "td": "word combination(s) in a sentence expressing syntactic connections "
                         "between words connected with traditions and those having destructive, demolishing and (or) "
                         "negatively evaluative components of meaning",
                   "ln": "words and word combinations provoking negative attitude to life in general",
                   "wsft": "euphemisms, well-sounding terms of foreign origination",
                   "fv": "words of foreign origination",
                   "spv": "word combination(s) in a sentence expressing syntactic connections "
                          "between the words naming power representatives, the symbols of state or power "
                          "and words having negative evaluative component of meaning, with the semantic of "
                          "destruction, violence and damage",
                   "pt": "present-tense forms of verbs",
                   "pasts": "past-tense forms of verbs",
                   "ft": "future-tense forms of verbs",
                   "ma": "modal adverbs",
                   "iw": "introductory words",
                   "hdg": "hedging",
                   "evmv": "verbs with evaluative components of meaning",
                   "trd": "information to be believed in the theme (theme/rheme division)",
                   "cu": '''adding to the rheme something "unexpected" for the addressee's culture''',
                   "parc": "parcelling",
                   "hrgw": "homogeneous rows, including those having generalizing words ",
                   "lcc": "long compositional constructions",
                   "scr": "relationships between the clauses",
                   "tpr": "repetitions of particular text parts",
                   "emdsd": '''Metaphors with  something causing fear, disgust and other negative feelings 
                   as the "source domain"  the thing the negative attitude to which is formed as "target domain"''',
                   "sppvf": "using second-personal pronouns and verb forms",
                   "aec": "appellation to an enemy country",
                   "rw": "Russian words",
                   "cm": "conjunctive mood"
                   }

imp_strats = ["l", "sia", "eud", "bvtmi", "ce", "dv", "dilu", "ema", "dea",
              "cfpa", "df", "utca", "piwl", "st", "dsps", "mc", "qii", "bep", "eip", "gco",
              "soes", "efc", "fns", "emms", "app", "rst"]

tags = ["b", "span", "section"]

type_tag_table = {'small': 'b', 'clausal': 'span', 'big': 'section'}


author_dir = "" #


# dict summing function


def sum_dicts(dct1, dct2):
    for key in dct2.keys():
        if key in dct1.keys() and type(dct1[key]) is int and type(dct2[key]) is int:
            dct1[key] += dct2[key]
        elif key in dct1.keys() and type(dct1[key]) is list and type(dct2[key]) is list:
            dct1[key].extend(dct2[key])
        elif key in dct1.keys() and type(dct1[key]) is dict and type(dct2[key]) is dict:
            sum_dicts(dct1[key], dct2[key])
        elif key not in dct1.keys():
            dct1[key] = dct2[key]
    return dct1

# counting the distribution of discoursive unit types (sizes)


def count_unit_type_stats_one_text(file_name):
    type_stats_dict = {}
    raw_content = open(os.path.join(author_dir, file_name), 'r', encoding='utf-8').read()
    soup = BeautifulSoup(raw_content, 'html.parser')
    for type in type_tag_table.keys():
        type_stats_dict[type] = len(soup.find_all(type_tag_table[type]))
    return type_stats_dict


# counting the number of times each strategy is implemented


def collect_unit_type_freq_dict_one_text(unit_type, file_name):
    raw_content = open(os.path.join(author_dir, file_name), 'r', encoding='utf-8').read()
    soup = BeautifulSoup(raw_content, 'html.parser')
    units = soup.find_all(type_tag_table[unit_type])
    freq_dict = {strat: 0 for strat in imp_strats}
    sep_strats = []
    for item in units:
        sep_strats += " ".join(item['class']).split("|")
    for sep_strat in sep_strats:
        freq_dict[sep_strat.split(" ")[0]] += 1
    return freq_dict


def collect_common_freq_dict_one_text(file_name):
    common_freq_dict = {strat: 0 for strat in imp_strats}
    for unit_type in type_tag_table.keys():
        one_type_dict = collect_unit_type_freq_dict_one_text(unit_type, file_name)
        common_freq_dict = {key: common_freq_dict[key] + one_type_dict[key] for key in common_freq_dict.keys()}
    return common_freq_dict


# counting the number of times each tactic (strategy realization means) is used


def collect_realization_statistics_unit_type_one_text(unit_type, file_name):
    raw_content = open(os.path.join(author_dir, file_name), 'r', encoding='utf-8').read()
    soup = BeautifulSoup(raw_content, 'html.parser')
    units = soup.find_all(type_tag_table[unit_type])
    freq_dict = {strat: dict() for strat in imp_strats}
    sep_strats = []
    for item in units:
        sep_strats += " ".join(item['class']).split("|")
    for sep_strat in sep_strats:
        if " ".join(sep_strat.split(" ")[1:]) not in freq_dict[sep_strat.split(" ")[0]].keys():
            freq_dict[sep_strat.split(" ")[0]][" ".join(sep_strat.split(" ")[1:])] = 1
        else:
            freq_dict[sep_strat.split(" ")[0]][" ".join(sep_strat.split(" ")[1:])] += 1
    return freq_dict


def collect_common_realization_statistics_one_text(file_name):
    common_dict = {strat: dict() for strat in imp_strats}
    for unit_type in type_tag_table.keys():
        one_type_dict = collect_realization_statistics_unit_type_one_text(unit_type, file_name)
        for key in common_dict.keys():
            common_dict[key] = sum_dicts(common_dict[key], one_type_dict[key])
    return common_dict


def collect_mean_realizing_text_parts_one_text(filename):
    strat_mean_text = {}
    raw_content = open(os.path.join(author_dir, filename), 'r', encoding='utf-8').read()
    soup = BeautifulSoup(raw_content, 'html.parser')
    real_stats = collect_common_realization_statistics_one_text(filename)
    for strat in real_stats.keys():
        if real_stats[strat].keys():
            for means in real_stats[strat].keys():
                strat_mean_text[strat + " " + means] = []
                template1 = "^" + strat + ' ' + means
                template2 = "\|" + strat + ' ' + means
                units = soup.find_all(class_=re.compile(template1)) + soup.find_all(class_=re.compile(template2))
                for unit in units:
                    for text_part in (list(unit.stripped_strings)):
                        strat_mean_text[strat + " " + means].append(text_part)
    return strat_mean_text


def collect_unit_type_stats_author(author_dir):
    author_type_stats_dict = {}
    for filename in os.listdir(author_dir):
        file_type_stats = count_unit_type_stats_one_text(filename)
        sum_dicts(author_type_stats_dict, file_type_stats)
    return author_type_stats_dict


def collect_common_freq_dict_author(author_dir):
    author_common_freq_dict = {}
    for filename in os.listdir(author_dir):
        file_freq_dict = collect_common_freq_dict_one_text(filename)
        sum_dicts(author_common_freq_dict, file_freq_dict)
    return author_common_freq_dict


def collect_common_realization_statistics_author(author_dir):
    author_realization_statistics_dict = {}
    for filename in os.listdir(author_dir):
        text_realization_statistics = collect_common_realization_statistics_one_text(filename)
        sum_dicts(author_realization_statistics_dict, text_realization_statistics)
    return author_realization_statistics_dict


def collect_mean_realizing_text_parts_author(author_dir):
    strat_mean_author = {}
    for filename in os.listdir(author_dir):
        strat_mean_text = collect_mean_realizing_text_parts_one_text(filename)
        sum_dicts(strat_mean_author, strat_mean_text)
    return strat_mean_author


def form_report(author_dir):
    report_file_name = os.path.split(author_dir)[-1] + '.txt'
    with open(report_file_name, 'w', encoding='utf-8') as report_file_obj:
        unit_type_stats = collect_unit_type_stats_author(author_dir)
        common_strategy_statistics = collect_common_freq_dict_author(author_dir)
        strategy_realization_means_statistics = collect_common_realization_statistics_author(author_dir)
        mean_realizing_text_parts = collect_mean_realizing_text_parts_author(author_dir)
        for key, value in unit_type_stats.items():
            report_file_obj.write("{} discoursive units performed impact strategies {} times\n".format(key, value))
        report_file_obj.write('+' * 50 + '\n')
        for key, value in common_strategy_statistics.items():
            if value != 0:
                report_file_obj.write('''The strategy of "{}" was realized in the texts {} times\n'''.format(strat_full_names[key], value))
        report_file_obj.write('+' * 50 + '\n')
        for key, value in strategy_realization_means_statistics.items():
            if value != {}:
                report_file_obj.write('''The "{}" strategy was realized with the help of the following means\n'''.format(strat_full_names[key]))
                for k, v in value.items():
                    if " " in k:
                        report_file_obj.write('''\t"{}": {} times\n'''.format(strat_full_names[k.split()[0]] + " " + mean_full_names[k.split()[1]], v))
                    else:
                        report_file_obj.write('''\t"{}": {} times\n'''.format(mean_full_names[k], v))
        report_file_obj.write('+' * 50 + '\n')
        report_file_obj.write("Here are the strategy realization examples:\n")
        for key, value in mean_realizing_text_parts.items():
            if len(key.split(" ")) == 2:
                report_file_obj.write("{} ({})\n".format(strat_full_names[key.split(" ")[0]], mean_full_names[key.split(" ")[1]]))
            elif len(key.split(" ")) == 3:
                report_file_obj.write("{}  ({} ({}))\n".format(strat_full_names[key.split(" ")[0]], strat_full_names[key.split(" ")[1]], mean_full_names[key.split(" ")[2]]))
            for fragment in value:
                report_file_obj.write('\t' + fragment + '\n')
                report_file_obj.write('-' * 40 + '\n')
        report_file_obj.write('+' * 50 + '\n')


form_report(author_dir)
