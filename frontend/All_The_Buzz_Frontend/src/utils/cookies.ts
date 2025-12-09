
export function getCookie(name: string): string | undefined {
    console.log('Getting cookie:', name);
    const target = `${encodeURIComponent(name)}=`
    const cookies = document.cookie ? document.cookie.split(';') : []
    for (let c of cookies) {
        c = c.trim()
        if (c.startsWith(target)) {
        return decodeURIComponent(c.substring(target.length))
        }
    }
}

