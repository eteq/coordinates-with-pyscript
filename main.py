# this is needed for conversions that need IERS data
import pyodide_http
pyodide_http.patch_all()

from astropy import coordinates

def populate_dropdowns(inelem, outelem):
    frame_names = coordinates.frame_transform_graph.get_names()
    frame_names.remove('icrs')
    frame_names.sort()
    frame_names.insert(0, 'icrs')

    select_options = [f'<option value="{nm}">{nm}</option>' for nm in frame_names]
    select_option_str = '\n  ' + '\n  '.join(select_options) + '\n'
    
    for e in (inelem, outelem):
        e.innerHTML = select_options


hin = Element("incoo")
hout = Element("outputcoo")
hinf = Element("inputframe")
houtf = Element("outputframe")
hbutton = Element("convertbutton")

populate_dropdowns(hinf.element, houtf.element)
hbutton.element.disabled = False

def convert():
    incoo = coordinates.SkyCoord(hin.element.value, 
                                 frame=hinf.element.value)
    toframe = houtf.element.value
    try:
        outcoo = incoo.transform_to(toframe)
    except Exception as e:
        hout.write(f"Failed to convert due to exception: {e}")
    else:
        hout.write(str(outcoo))