import pdfMake from 'pdfmake/build/pdfmake'
import 'pdfmake/build/vfs_fonts'

// pdfMake.vfs = pdfFonts.pdfMake.vfs

// page numbers

let styles = {
  header: {
    fontSize: 18,
    bold: true,
    alignment: 'center',
    margin: [0, 10, 0, 5]
  },
  subheader: {
    fontSize: 12,
    bold: true,
    alignment: 'center',
    margin: [0, 5, 0, 5]
  },
  styleheader: {
    fontSize: 12,
    bold: true,
    alignment: 'left',
    margin: [0, 4, 0, 1],
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
    Array.from(new Set(p_table.data.map(p => p.session))).map((session, i) => {
      if (i == 0) {
        docDefinition.content.push({ text: session, style: 'header' })
      } else {
        docDefinition.content.push({ text: session, style: 'header', pageBreak: 'before' })
      }
      let targetGrp = p_table.data.filter(p => p.session === session)
      docDefinition.content.push({
        table: {
          headerRows: 0,
          widths: [75, '*'],
          dontBreakRows: true,
          body: Array.from(new Set(targetGrp.map(p => p.target))).sort( function(a, b) {return a - b}).map(end => {
            return [{text: end, style: 'endTitle'}, {
              layout: 'noBorders',
              table: {
                headerRows: 0,
                widths: [125, '*', '*', '*', '*'],
                body: [
                  ...targetGrp.filter(p => p.target === end).sort(function (a, b) {return a.pos < b.pos ? -1 : a.pos > b.pos ? 1 : 0}).map(p => {
                    return [p.name, p.club, p.class, p.pos, p.sum > 0 ? p.sum : '']
                  })
                ]
              }
            }]
          })
        }
      })
    })
    pdfMake.createPdf(docDefinition).open()
  },
  results2pdf(event, r_table) {
    let widths = ['auto']
    if (event.use_level_class) {
      widths.push('auto')
    }
    widths.push(...[98, 28, ...Array(r_table.meta.rounds.length).fill('*')])
    if (r_table.meta.spots) {
      widths.push(...Array(r_table.meta.spots).fill(18))
    }
    widths.push(24)
    if (r_table.meta.so) {
      widths.push('auto')
    }

    let docDefinition = {
      pageSize: 'A4',
      footer: function(currentPage, pageCount) {
        return {
          columns: [
            { text: window.location.origin + '/#' + r_table.meta.url, style: 'footer' },
            { text: currentPage + ' of ' + pageCount, alignment: 'center'},
            { text: new Date().toLocaleString(), alignment: 'right', style: 'footer' }
          ],
        }
      },
      content: [
        {text: event.name, style: 'header'},
        {
          layout: 'noBorders',
          table: {
            headerRows: 0,
            widths: ['auto', 'auto', '*', 'auto', 'auto'],
            body: [
              [{text: 'Location'}, {text: event.location}, {}, {text: 'Organizer'}, {text: event.organizer}],
              [{text: 'Referees'}, {text: event.judges}, {}, {text: 'Date'}, {text: event.date_start + (event.date_start !== event.date_end ? ' -- ' + event.date_end : '')}]
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
                        {text: m[2], fontSize: 6, 'alignment': 'left'}
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
  },
  roundResults2pdf(event, round_table) {
    let docDefinition = {
      pageSize: {
        // width: 842,
        width: 475 + 28 * round_table.meta.ends,
        height: 595,
      },
      footer: function(currentPage, pageCount) {
        return {
          columns: [
            { text: window.location.origin + '/#' + round_table.meta.url, style: 'footer' },
            { text: currentPage + ' of ' + pageCount, alignment: 'center'},
            { text: new Date().toLocaleString(), alignment: 'right', style: 'footer' }
          ],
        }
      },
      content: [
        {text: event.name, style: 'styleheader'},
        {text: round_table.meta.round_label, alignment: 'left', fontSize: 12},
        {
          layout: 'noBorders',
          table: {
            headerRows: 0,
            widths: ['auto', 'auto', 'auto', 'auto'],
            body: [
              [{text: 'Location'}, {text: event.location}, {text: 'Organizer'}, {text: event.organizer}],
              [{text: 'Referees'}, {text: event.judges}, {text: 'Date'}, {text: event.date_start + (event.date_start !== event.date_end ? ' -- ' + event.date_end : '')}]
            ]
          }
        },
        Array.from(new Set(round_table.data.map(r => r.class))).map(cls => {
          return {
            layout: 'lightHorizontalLines',
            table: {
              headerRows: 2,
              widths: round_table.header.filter(h => h.value !== 'class').map(h => h.pdf_width),
              body: [
                [{text: cls, colSpan: round_table.header.length - 1, style: 'styleheader' },
                 ...Array(round_table.header.length - 2).fill('')],

                round_table.header.filter(h => h.value !== 'class').map(h => {
                  return {text: h.text, style: 'tableheader'}
                }),

                ...round_table.data.filter(r => r.class === cls).map(r => {
                  return round_table.header.filter(h => h.value !== 'class').map(h => {
                    if (typeof(r[h.value]) === 'undefined') {
                      return ''
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
