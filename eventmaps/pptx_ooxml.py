"""Minimal OOXML PresentationML writer — no third-party dependencies.

A .pptx is a ZIP of XML parts. python-pptx is not installable in this
environment (no pip), and vendoring it for one script is not worth it, so this
module writes the handful of parts a slide deck actually needs:

    [Content_Types].xml  _rels/.rels  docProps/{core,app}.xml
    ppt/presentation.xml + rels
    ppt/slideMasters/slideMaster1.xml + rels
    ppt/slideLayouts/slideLayout1.xml + rels      (one blank layout)
    ppt/theme/theme1.xml
    ppt/slides/slideN.xml + rels                  (one per slide)

Everything is positioned absolutely in EMU, which suits a worksheet: each
organizer box is a real autoshape with a real text frame, so a teacher can
retype a prompt, drag a box, or click in and type an answer.

Coordinates in the public API are INCHES; conversion to EMU happens here.
"""
import zipfile
from xml.sax.saxutils import escape

EMU_PER_INCH = 914400
NS_R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'


def emu(inches):
    return int(round(inches * EMU_PER_INCH))


def _esc(text):
    return escape(str(text))


# --------------------------------------------------------------------------
# Shape builders. Each returns one <p:sp> element.
# --------------------------------------------------------------------------

def _text_body(paragraphs, *, align='l', anchor='t', wrap=True,
               ins=(0.05, 0.03, 0.05, 0.03), rtl=False, autofit=False):
    """paragraphs: list of (text, size_pt, bold) tuples."""
    l, t, r, b = (emu(v) for v in ins)
    fit = '<a:normAutofit/>' if autofit else ''
    body = (f'<a:bodyPr lIns="{l}" tIns="{t}" rIns="{r}" bIns="{b}" '
            f'anchor="{anchor}" wrap="{"square" if wrap else "none"}">{fit}</a:bodyPr>'
            '<a:lstStyle/>')
    if not paragraphs:
        paragraphs = [('', 10, False)]
    for text, size, bold in paragraphs:
        ppr = f'<a:pPr algn="{align}"{" rtl=\"1\"" if rtl else ""}/>'
        runs = ''
        # A literal newline inside one paragraph is a soft break.
        parts = str(text).split('\n')
        for i, part in enumerate(parts):
            if i:
                runs += '<a:br/>'
            if part == '':
                continue
            runs += (
                f'<a:r><a:rPr lang="en-US" sz="{int(round(size * 100))}" '
                f'b="{1 if bold else 0}" dirty="0">'
                '<a:solidFill><a:srgbClr val="111111"/></a:solidFill>'
                '<a:latin typeface="Arial"/><a:cs typeface="Arial"/></a:rPr>'
                f'<a:t>{_esc(part)}</a:t></a:r>')
        if not runs:
            runs = '<a:endParaRPr lang="en-US"/>'
        body += f'<a:p>{ppr}{runs}</a:p>'
    return f'<p:txBody>{body}</p:txBody>'


def shape(sid, name, x, y, w, h, *, geom='roundRect', adj=None,
          line_w_pt=1.5, dash=None, paragraphs=(), align='l', anchor='t',
          rtl=False, fill=None):
    """A bordered autoshape with an editable text frame."""
    av = ''
    if adj is not None:
        av = f'<a:gd name="adj" fmla="val {int(adj)}"/>'
    dash_xml = f'<a:prstDash val="{dash}"/>' if dash else ''
    fill_xml = (f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>'
                if fill else '<a:noFill/>')
    ln = (f'<a:ln w="{int(round(line_w_pt * 12700))}" cap="flat">'
          f'<a:solidFill><a:srgbClr val="111111"/></a:solidFill>{dash_xml}</a:ln>')
    return (
        '<p:sp><p:nvSpPr>'
        f'<p:cNvPr id="{sid}" name="{_esc(name)}"/><p:cNvSpPr/><p:nvPr/>'
        '</p:nvSpPr><p:spPr>'
        f'<a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/>'
        f'<a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>'
        f'<a:prstGeom prst="{geom}"><a:avLst>{av}</a:avLst></a:prstGeom>'
        f'{fill_xml}{ln}</p:spPr>'
        + _text_body(list(paragraphs), align=align, anchor=anchor, rtl=rtl)
        + '</p:sp>')


def textbox(sid, name, x, y, w, h, *, paragraphs=(), align='l', anchor='t',
            rtl=False, wrap=True):
    """Borderless, fill-less text — headings, labels, the footer."""
    return (
        '<p:sp><p:nvSpPr>'
        f'<p:cNvPr id="{sid}" name="{_esc(name)}"/>'
        '<p:cNvSpPr txBox="1"/><p:nvPr/>'
        '</p:nvSpPr><p:spPr>'
        f'<a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/>'
        f'<a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        '<a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>'
        + _text_body(list(paragraphs), align=align, anchor=anchor, rtl=rtl,
                     wrap=wrap, ins=(0.02, 0.01, 0.02, 0.01))
        + '</p:sp>')


def line(sid, name, x, y, w, *, line_w_pt=1.0):
    """A horizontal rule (the header underline, the footer rule)."""
    return (
        '<p:cxnSp><p:nvCxnSpPr>'
        f'<p:cNvPr id="{sid}" name="{_esc(name)}"/><p:cNvCxnSpPr/><p:nvPr/>'
        '</p:nvCxnSpPr><p:spPr>'
        f'<a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/>'
        f'<a:ext cx="{emu(w)}" cy="0"/></a:xfrm>'
        '<a:prstGeom prst="line"><a:avLst/></a:prstGeom>'
        f'<a:ln w="{int(round(line_w_pt * 12700))}">'
        '<a:solidFill><a:srgbClr val="111111"/></a:solidFill></a:ln>'
        '</p:spPr></p:cxnSp>')


# --------------------------------------------------------------------------
# Package assembly
# --------------------------------------------------------------------------

_THEME = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Office">
<a:themeElements>
<a:clrScheme name="Office"><a:dk1><a:sysClr val="windowText" lastClr="000000"/></a:dk1>
<a:lt1><a:sysClr val="window" lastClr="FFFFFF"/></a:lt1>
<a:dk2><a:srgbClr val="023266"/></a:dk2><a:lt2><a:srgbClr val="F4F8FC"/></a:lt2>
<a:accent1><a:srgbClr val="054C8C"/></a:accent1><a:accent2><a:srgbClr val="FBD239"/></a:accent2>
<a:accent3><a:srgbClr val="238A8D"/></a:accent3><a:accent4><a:srgbClr val="6D5AA8"/></a:accent4>
<a:accent5><a:srgbClr val="D97A28"/></a:accent5><a:accent6><a:srgbClr val="5A8F52"/></a:accent6>
<a:hlink><a:srgbClr val="054C8C"/></a:hlink><a:folHlink><a:srgbClr val="6D5AA8"/></a:folHlink></a:clrScheme>
<a:fontScheme name="Office">
<a:majorFont><a:latin typeface="Arial"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>
<a:minorFont><a:latin typeface="Arial"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont></a:fontScheme>
<a:fmtScheme name="Office">
<a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
<a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>
<a:lnStyleLst>
<a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/></a:ln>
<a:ln w="12700"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/></a:ln>
<a:ln w="19050"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/></a:ln></a:lnStyleLst>
<a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle>
<a:effectStyle><a:effectLst/></a:effectStyle>
<a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>
<a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
<a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme>
</a:themeElements><a:objectDefaults/><a:extraClrSchemeLst/></a:theme>'''

_MASTER = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
 xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
<p:cSld><p:bg><p:bgPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>
<p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>
<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>
<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2"
 accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6"
 hlink="hlink" folHlink="folHlink"/>
<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>
</p:sldMaster>'''

_LAYOUT = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
 xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
 type="blank" preserve="1">
<p:cSld name="Blank"><p:spTree>
<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>
<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>
<p:clrMapOvr><a:overrideClrMapping bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2"
 accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4"
 accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/></p:clrMapOvr>
</p:sldLayout>'''


def _slide_xml(shapes_xml):
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
        ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
        ' xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
        '<p:cSld><p:spTree>'
        '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
        '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
        '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
        + shapes_xml +
        '</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>')


def write_pptx(path, slides, *, width_in=11.0, height_in=8.5,
               title='Presentation'):
    """slides: list of shape-XML strings, one per slide."""
    n = len(slides)
    rels = ''.join(
        f'<Relationship Id="rId{i + 2}" Type="{NS_R}/slide" '
        f'Target="slides/slide{i + 1}.xml"/>' for i in range(n))
    sld_ids = ''.join(
        f'<p:sldId id="{256 + i}" r:id="rId{i + 2}"/>' for i in range(n))

    presentation = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
        ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
        ' xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
        ' saveSubsetFonts="1">'
        '<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
        f'<p:sldIdLst>{sld_ids}</p:sldIdLst>'
        f'<p:sldSz cx="{emu(width_in)}" cy="{emu(height_in)}"/>'
        f'<p:notesSz cx="{emu(height_in)}" cy="{emu(width_in)}"/>'
        '</p:presentation>')

    ct = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>'
          '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>'
          '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>'
          '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
          '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
          '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>']
    for i in range(n):
        ct.append(f'<Override PartName="/ppt/slides/slide{i + 1}.xml" '
                  'ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>')
    ct.append('</Types>')

    core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"'
            ' xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/"'
            ' xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            f'<dc:title>{_esc(title)}</dc:title>'
            '<dc:creator>Miguel Guhlin / Miguel Guhlin</dc:creator>'
            '<cp:lastModifiedBy>Miguel Guhlin</cp:lastModifiedBy>'
            '</cp:coreProperties>')

    app = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"'
           ' xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
           f'<Application>History Event Maps</Application><Slides>{n}</Slides>'
           '</Properties>')

    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', ''.join(ct))
        z.writestr('_rels/.rels',
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   f'<Relationship Id="rId1" Type="{NS_R}/officeDocument" Target="ppt/presentation.xml"/>'
                   '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
                   f'<Relationship Id="rId3" Type="{NS_R}/extended-properties" Target="docProps/app.xml"/>'
                   '</Relationships>')
        z.writestr('docProps/core.xml', core)
        z.writestr('docProps/app.xml', app)
        z.writestr('ppt/presentation.xml', presentation)
        z.writestr('ppt/_rels/presentation.xml.rels',
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   f'<Relationship Id="rId1" Type="{NS_R}/slideMaster" Target="slideMasters/slideMaster1.xml"/>'
                   + rels +
                   f'<Relationship Id="rId{n + 2}" Type="{NS_R}/theme" Target="theme/theme1.xml"/>'
                   '</Relationships>')
        z.writestr('ppt/theme/theme1.xml', _THEME)
        z.writestr('ppt/slideMasters/slideMaster1.xml', _MASTER)
        z.writestr('ppt/slideMasters/_rels/slideMaster1.xml.rels',
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   f'<Relationship Id="rId1" Type="{NS_R}/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
                   f'<Relationship Id="rId2" Type="{NS_R}/theme" Target="../theme/theme1.xml"/>'
                   '</Relationships>')
        z.writestr('ppt/slideLayouts/slideLayout1.xml', _LAYOUT)
        z.writestr('ppt/slideLayouts/_rels/slideLayout1.xml.rels',
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   f'<Relationship Id="rId1" Type="{NS_R}/slideMaster" Target="../slideMasters/slideMaster1.xml"/>'
                   '</Relationships>')
        for i, shapes_xml in enumerate(slides):
            z.writestr(f'ppt/slides/slide{i + 1}.xml', _slide_xml(shapes_xml))
            z.writestr(f'ppt/slides/_rels/slide{i + 1}.xml.rels',
                       '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                       '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                       f'<Relationship Id="rId1" Type="{NS_R}/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
                       '</Relationships>')
