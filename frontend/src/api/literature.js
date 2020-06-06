import request from "../utils/request";

export function getLiterature(query) {
  return request({
    url: "http://s.c/literature/search",
    method: "get",
    params: query,
  });
}

export function getSources() {
  return request({
    url: "http://s.c/literature/getSources",
    method: "get",
  });
}
