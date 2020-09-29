import pdfMake from 'pdfmake/build/pdfmake'
import pdfFonts from 'pdfmake/build/vfs_fonts'

pdfMake.vfs = pdfFonts.pdfMake.vfs

let styles = {
  header:{
    fontSize: 24,
    bold: true,
    alignment: 'center',
    margin: [0, 15, 0, 5]
  },
  subheader: {
    fontSize: 16,
    bold: true,
    alignment: 'center',
    margin: [0, 5, 0, 5]
  },
  styleheader: {
    fontSize: 18,
    bold: true,
    margin: [0, 15, 0, 5]
  },
  footer: {
    fontSize: 10,
    margin: [5, 0, 5, 0]
  }
}

export default {
  endAssignments2pdf(event, p_table, url) {
    let docDefinition = {
      pageSize: 'A4',
      footer: {
        columns: [
          { text: window.location.origin + '/#' + url, style: 'footer' },
          { text: new Date().toLocaleString(), alignment: 'right', style: 'footer' }
        ]
      },
      content: [{text: event.name, style: 'header'}],
      styles: Object.assign({
        endTitle: {
          fontSize: 32,
          bold: true,
          alignment: 'center',
          margin: [0, 20, 0, 20]
        }
      }, styles)
    }
    for (let group of Array.from(new Set(p_table.data.map(p => p.group)))) {
      docDefinition.content.push({text: group, style: 'styleheader'})
      let groupGrp = p_table.data.filter(p => p.group === group)
      docDefinition.content.push({
        table: {
          headerRows: 0,
          widths: [75, '*'],
          dontBreakRows: true,
          body: Array.from(new Set(groupGrp.map(p => p.end))).sort( function(a, b) {return a - b}).map(end => {
            return [{text: end, style: 'endTitle'}, {
              layout: 'noBorders',
              table: {
                headerRows: 0,
                widths: [125, '*', '*', '*'],
                body: [
                  ...groupGrp.filter(p => p.end === end).sort(function (a, b) {return a.pos < b.pos ? -1 : a.pos > b.pos ? 1 : 0}).map(p => {
                    return [p.name, p.class, p.pos, p.sum > 0 ? p.sum : '']
                  })
                ]
              }
            }]
          })
        }
      })
    }
    pdfMake.createPdf(docDefinition).open()
  },
  results2pdf(event, r_table, url ) {
    let docDefinition = {
      pageOrientation: event.rounds.length > 2 ? 'landscape' : 'portrait',
      footer: {
        columns: [
          { text: window.location.origin + '/#' + url, style: 'footer' },
          { text: new Date().toLocaleString(), alignment: 'right', style: 'footer' }
        ]
      },
      content: [{text: event.name, style: 'header'},
        Array.from(new Set(r_table.data.map(r => r.class))).map(cls => {
        return {
          layout: 'lightHorizontalLines',
          table: {
            headerRows: 2,
            widths: [30, 125, 30, ...Array(r_table.header.length - 4).fill('*')],
            body: [
              [{text: cls, colSpan: r_table.header.length - 1, style: 'styleheader' },
               ...Array(r_table.header.length - 2).fill('')],

              r_table.header.filter(h => h.value !== 'class').map(h => {
                return {text: h.text, style: 'tableheader'}
              }),

              ...r_table.data.filter(r => r.class === cls).map(r => {
                return r_table.header.filter(h => h.value !== 'class').map(h => {
                  if (typeof(r[h.value]) === 'undefined') {
                    return ''
                  }
                  if (typeof(r[h.value]) === 'string' && r[h.value].match(/<sup>(\d)<\/sup>/)) {
                    let m = r[h.value].match(/(\d+)<sup>(\d)<\/sup>/)
                    return {columns: [
                      {text: m[1], width: 'auto'},
                      {text: m[2], fontSize: 8}
                    ]}
                  }
                  return h.value === 'sum' ? {text: r[h.value], bold: true} : r[h.value]
                })
              })
            ]
          }
        }
      })],
      styles: Object.assign({
        tableheader: {
          fontSize: 12,
          bold: true,
          margin: [0, 0, 0, 0]
        }
      }, styles),
    }
    pdfMake.createPdf(docDefinition).open()
  }
}
