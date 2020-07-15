export default {
  sum(arr) {
    return Array.isArray(arr) && arr.length ? arr.reduce((sum, x) => sum + x) : null;
  },
  participantOrder( a, b ) {
    if ( a.class < b.class) {
      return -1;
    }
    if ( a.class > b.class) {
      return 1;
    }
    if ( a.sum > b.sum ){
      return -1;
    }
    if ( a.sum < b.sum ){
      return 1;
    }
    if (a.shootoff && b.shootoff) {
      if (a.shootoff > b.shootoff) {
        return -1;
      }
      if (a.shootoff < b.shootoff) {
        return 1;
      }
    } else {
      if (a.x > b.x) {
        return -1;
      }
      if (a.x < b.x) {
        return 1;
      }
    }
    return 0;
  },
  participantRank(p_list) {
    let place = {class: null, ord: 1, sum: null, x: null}
    for (let p of p_list.sort( this.participantOrder )) {
      if (p.class !== place.class) {
        place.class = p.class
        place.ord = 1
        place.place = 1
        place.sum = p.sum
        place.x = p.x
      }
      if (p.sum < place.sum) {
        place.place = place.ord
      } else if (p.shootoff) {
        place.place = place.ord
      } else if (p.x < place.x && place.ord > 3) {
        place.place = place.ord
      }
      p['place'] = place.place
      place.x = p.x
      place.sum = p.sum
      place.ord += 1
    }
  },
  getClass(p, ops) {
    // p is participant
    if (ops && ops.includes(p.age_group + '_' + p.style)) {
      return p.age_group + '_' + p.style
    }
    return p.age_group + p.archer.gender + p.style
  }
}
