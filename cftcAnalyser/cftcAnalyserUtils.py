def write_start_of_metric_html_file(f):
    f.write('<!DOCTYPE html>\n')
    f.write('<html>\n')
    f.write('<head>\n')
    f.write('<style>\n')
    f.write('table {\n')
    f.write('border-collapse: collapse;\n')
    f.write('border: 2px solid black;\n')
    f.write('width: 100%;\n')
    f.write('}\n')
    f.write('th {\n')
    f.write('border: 2px solid black;\n')
    f.write('text-align: center;\n')
    f.write('}\n')
    f.write('td {\n')
    f.write('border: 1px solid black;\n')
    f.write('text-align: center;\n')
    f.write('}\n')
    f.write('</style>\n')
    f.write('</head>\n')
    f.write('<body>\n')
    f.write('<h2>METRICS</h2>\n')
    f.write('<table>\n')
    f.write('<tr>\n')
    f.write('<th width=\"20%\">Metric</th>\n')
    f.write('<th width=\"10%\">Latest</th>\n')
    f.write('<th width=\"10%\">W/W change</th> \n')
    f.write('<th width=\"10%\">3M Ave</th>\n')
    f.write('<th width=\"10%\">6M Ave</th>\n')
    f.write('<th width=\"10%\">1Y Ave</th>\n')
    f.write('<th width=\"10%\">3Y Max</th>\n')
    f.write('<th width=\"10%\">3Y Min</th>\n')
    f.write('<th width=\"5%\">1Y</th>\n')
    f.write('<th width=\"5%\">3Y</th>\n')
    f.write('</tr>\n')

def _get_string_representation_of_number(string_format, number):
    if number < 0:
        return_format = "(%s)" % string_format % abs(number)
    else:
        return_format = "%s" % string_format % number
    return return_format

THRESHOLD_VALUE = 1.5
RED = "bgcolor=\"#FF4040\""
GREEN = "bgcolor=\"#40FF40\""

def write_line_in_metric_html_file(f, metric, latest, ww_change, three_month_avg, six_month_avg, one_year_avg, maximum, minimum, z_score_one_year, z_score_three_years, path_to_graph):
    f.write('<tr>\n')
    f.write('<td><a href=\"file:///%s\" target=\"_blank\">%s</td>\n' % (path_to_graph, metric))
    f.write('<td>%s</td>\n' % _get_string_representation_of_number("%d", latest))
    f.write('<td>%s</td>\n' % _get_string_representation_of_number("%d", ww_change))
    f.write('<td>%s</td>\n' % _get_string_representation_of_number("%d", three_month_avg))
    f.write('<td>%s</td>\n' % _get_string_representation_of_number("%d", six_month_avg))
    f.write('<td>%s</td>\n' % _get_string_representation_of_number("%d", one_year_avg))
    f.write('<td>%s</td>\n' % _get_string_representation_of_number("%d", maximum))
    f.write('<td>%s</td>\n' % _get_string_representation_of_number("%d", minimum))
    if z_score_one_year > THRESHOLD_VALUE:
        f.write('<td %s>%0.2f</td>\n' % (GREEN, z_score_one_year))
    elif z_score_one_year < -THRESHOLD_VALUE:
        f.write('<td %s>%0.2f</td>\n' % (RED, z_score_one_year))
    else:
        f.write('<td>%0.2f</td>\n' % z_score_one_year)
    if z_score_three_years > THRESHOLD_VALUE:
        f.write('<td %s>%0.2f</td>\n' % (GREEN, z_score_three_years))
    elif z_score_three_years < -THRESHOLD_VALUE:
        f.write('<td %s>%0.2f</td>\n' % (RED, z_score_three_years))
    else:
        f.write('<td>%0.2f</td>\n' % z_score_three_years)
    f.write('</tr>\n')

def write_end_of_metric_html_file(f):
    f.write('</table>\n')
    f.write('</body>\n')
    f.write('</html>\n')
