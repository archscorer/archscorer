import pdfMake from 'pdfmake/build/pdfmake'
import pdfFonts from 'pdfmake/build/vfs_fonts'

pdfMake.vfs = pdfFonts.pdfMake.vfs

let styles = {
  header: {
    fontSize: 18,
    bold: true,
    alignment: 'center',
    margin: [0, 15, 0, 5]
  },
  subheader: {
    fontSize: 12,
    bold: true,
    alignment: 'center',
    margin: [0, 5, 0, 5]
  },
  styleheader: {
    fontSize: 14,
    bold: true,
    alignment: 'left',
    margin: [0, 15, 0, 5],
  },
  footer: {
    fontSize: 8,
    alignment: 'left',
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
          margin: [0, 16, 0, 16]
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
  results2pdf(event, r_table) {
    let widths = ['auto']
    if (event.use_level_class) {
      widths.push('auto')
    }
    widths.push(...[98, 28, ...Array(r_table.meta.rounds).fill('*')])
    if (r_table.meta.spots) {
      widths.push(...Array(r_table.meta.spots).fill(18))
    }
    widths.push('auto')
    if (r_table.meta.so) {
      widths.push('auto')
    }

    let docDefinition = {
      footer: {
        columns: [
          { text: window.location.origin + '/#' + r_table.meta.url, style: 'footer' },
          { text: new Date().toLocaleString(), alignment: 'right', style: 'footer' }
        ]
      },
      content: [
        {text: event.name, style: 'header'},
        {
          layout: 'noBorders',
          table: {
            headerRows: 0,
            widths: ['auto', 'auto'],
            body: [
              [{text: 'Location'}, {text: event.location}],
              [{text: 'Organizer'}, {text: event.organizer}],
              [{text: 'Date'}, {text: event.date_start + (event.date_start !== event.date_end ? ' -- ' + event.date_end : '')}]
            ]
          }
        },
        Array.from(new Set(r_table.data.map(r => r.class))).map(cls => {
          return {
            layout: 'lightHorizontalLines',
            table: {
              headerRows: 2,
              widths: widths,
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
                        {text: m[2], fontSize: 6}
                      ]}
                    }
                    return h.value === 'sum' ? {text: r[h.value], bold: true} : r[h.value]
                  })
                })
              ]
            }
          }
        })
      ],
      styles: Object.assign({
        tableheader: {
          fontSize: 9,
          bold: true,
          margin: [0, 0, 0, 0]
        }
      }, styles),
      defaultStyle: {
        fontSize: 9,
        alignment: 'right',
      }
    }
    pdfMake.createPdf(docDefinition).open()
  }
}
