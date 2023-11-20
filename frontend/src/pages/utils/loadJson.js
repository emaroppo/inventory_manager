async function loadJson(path) {
    const response = await fetch(path);
    const data = await response.json();
    return data;
}

export default loadJson;