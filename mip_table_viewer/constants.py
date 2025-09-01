# (C) British Crown Copyright 2022, Met Office.
# Please see LICENSE.rst for license details.
HEADINGS = ['Mip Table', 'Variable Name', 'Frequency', 'Dimensions', 'Standard Name', 'Long Name', 'Comment', 'Modeling Realm', 'Units', 'Positive', 'Cell Methods', 'Cell Measures']
HEADER_ROW_TEMPLATE = '  <thead><tr bgcolor="{}">\n{}  </tr></thead>\n'
ROW_TEMPLATE = '  <tr bgcolor="{}">\n{}  </tr>\n'
CELL_TEMPLATE = '   <{0}>{1}</{0}>\n'
TABLE_TEMPLATE = '<table border=1, id="table_id", class="display">\n{}</table>\n'
BGCOLORS = ['#E0EEFF', '#FFFFFF']
HEADER = """
<html>
<head>
<link rel="stylesheet" type="text/css" charset="UTF-8" href="https://cdn.datatables.net/2.3.2/css/dataTables.dataTables.min.css" />
<script type="text/javascript" charset="UTF-8" src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script type="text/javascript" charset="UTF-8" src="https://cdn.datatables.net/2.3.2/js/dataTables.min.js"></script>
<script type="text/javascript">
//<![CDATA[
$(document).ready( function () {
    $('#table_id').DataTable({"pageLength": 100});
    } );
//]]>
</script>
</head>
<body>"""

FOOTER = """
</body>
</html>"""

WRAP_SIZE = 54
