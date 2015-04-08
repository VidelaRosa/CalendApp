/*"""
Copyright 2015 Victor de la Rosa Sanchez
This file is part of CalendApp.

    CalendApp is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License.

    CalendApp is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with CalendApp.  If not, see <http://www.gnu.org/licenses/>.
"""*/
$(document).ready(function() {
    $('#searchdatepicker').datetimepicker({
        locale: 'es',
        format: 'L'
    });
    $('#datepicker').datetimepicker({
        locale: 'es',
        format: 'L'
    });
    $('#timepicker').datetimepicker({
        locale: 'es',
        format: 'LT'
    });
});