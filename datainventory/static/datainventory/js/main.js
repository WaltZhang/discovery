
function addTable(list, appendObj, schema) {
    var columns = addAllColumnHeaders(list, appendObj, schema);

    for (var i = 0; i < list.length; i++) {
        var row$ = $('<tr/>');
        for (var colIndex = 0; colIndex < columns.length; colIndex++) {
            var cellValue = list[i][columns[colIndex]];

            if (cellValue == null) {
                cellValue = "";
            }

            if (cellValue.constructor === Array)
            {
                $a = $('<td/>');
                row$.append($a);
                addTable(cellValue, $a);

            } else if (cellValue.constructor === Object)
            {

                var array = $.map(cellValue, function (value, index) {
                    return [value];
                });

                $a = $('<td/>');
                row$.append($a);
                addObject(array, $a);

            } else {
                row$.append($('<td/>').html(cellValue));
            }
        }
        appendObj.append(row$);
    }
}


function addObject(list, appendObj) {
    for (var i = 0; i < list.length; i++) {
        var row$ = $('<tr/>');

        var cellValue = list[i];

        if (cellValue == null) {
            cellValue = "";
        }

        if (cellValue.constructor === Array)
        {
            $a = $('<td/>');
            row$.append($a);
            addTable(cellValue, $a);

        } else if (cellValue.constructor === Object)
        {

            var array = $.map(cellValue, function (value, index) {
                return [value];
            });

            $a = $('<td/>');
            row$.append($a);
            addObject(array, $a);

        } else {
            row$.append($('<td/>').html(cellValue));
        }
        appendObj.append(row$);
    }
}

// Adds a header row to the table and returns the set of columns.
// Need to do union of keys from all records as some records may not contain
// all records
function addAllColumnHeaders(list, appendObj, schemaObj)
{
    var columnSet = [];
    var headerTr$ = $('<tr/>');
    var schema = $.parseJSON(schemaObj.val());

    for (var i = 0; i < list.length; i++) {
        var rowHash = list[i];
        for (var key in rowHash) {
            if ($.inArray(key, columnSet) == -1) {
                columnSet.push(key);
                var value = "string";
                $.each(schema, function(i, obj) {
                    if (obj.hasOwnProperty(key)) {
                        value = obj[key];
                    }
                });
                headerTr$.append($('<th/>')//.html(key));
                    .append(key, addTypeMenu(value, key, schemaObj)));
            }
        }
    }
    appendObj.append(headerTr$);

    return columnSet;
}

function addTypeMenu(type, title, schemaObj)
{
    var select = $('<select/>');
    select.attr('id', title);
    select.change(function(event) { updateSchema(schemaObj, $(this)); });
    if (type == "string")
        select.append($('<option value="string" selected/>').html('String'));
    else
        select.append($('<option value="string"/>').html('String'));
    if (type == "int")
        select.append($('<option value="tinyint" selected/>').html('Byte'));
    else
        select.append($('<option value="tinyint"/>').html('Byte'));
    if (type == "int")
        select.append($('<option value="smallint" selected/>').html('Short'));
    else
        select.append($('<option value="smallint"/>').html('Short'));
    if (type == "int")
        select.append($('<option value="int" selected/>').html('Integer'));
    else
        select.append($('<option value="int"/>').html('Integer'));
    if (type == "bigint")
        select.append($('<option value="bigint" selected/>').html('Long'));
    else
        select.append($('<option value="bigint"/>').html('Long'));
    if (type == "Date")
        select.append($('<option value="date" selected/>').html('Date'));
    else
        select.append($('<option value="date"/>').html('Date'));
    if (type == "Time")
        select.append($('<option value="timestamp" selected/>').html('Time'));
    else
        select.append($('<option value="timestamp"/>').html('Time'));
    return select;
}

function updateSchema(schemaObj, component)
{
    var k = component.attr("id");
    var v = component.val();
    var schema = $.parseJSON(schemaObj.attr('value'));
    for (var i = 0; i < schema.length; ++i) {
        if (schema[i].hasOwnProperty(k)) {
            schema[i][k] = v;
        }
    }
    schemaObj.attr('value', JSON.stringify(schema));
    console.log(schemaObj.val());
}
