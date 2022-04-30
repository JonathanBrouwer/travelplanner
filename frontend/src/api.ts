
const API_URL = "http://localhost:8081"

export interface Point {
    lat: number,
    lng: number,
}

function onError(reason: any) {
    console.error(reason);
    return null;
}

function filterError<T>(o: T): T | null {
    if ((o as any).hasOwnProperty("error")) {
        onError((o as any)["error"]);
        return null;
    } else {
        return o;
    }
}

export async function getClosestPoint(p: Point): Promise<Point | null> {
    try {
        const res = await fetch(`/closest_point/`, {
            credentials: "include",
            method: "POST",
            body: JSON.stringify(p)
        });
        return filterError(await res.json());
    } catch (e) {
        return onError(e);
    }
}

