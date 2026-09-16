import axios from "axios";

const BASE_URL = process.env.BASE_URL;
const USERNAME = process.env.USERNAME;
const PASSWORD = process.env.PASSWORD;

if (!BASE_URL || !USERNAME || !PASSWORD) {
  throw new Error(
    "Missing required environment variables: BASE_URL, USERNAME, PASSWORD"
  );
}

const client = axios.create({
  baseURL: BASE_URL,
  timeout: 15000,
  maxRedirects: 5,
  validateStatus: () => true,
  headers: {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36 Edg/153.0.0.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    "content-type":"application/x-www-form-urlencoded"
    "cookie":"_safe=PqndvTcraOCvF7Aa; kt_lang=zh; deviceId=dev_svk445tgtj; kt_tcookie=1; cw_conversation=eyJhbGciOiJIUzI1NiJ9.eyJzb3VyY2VfaWQiOiIwZmVjZmY2NS02Yjc2LTQ0NjItODQ4NC0wZmVjMGNmYzE5ZmYiLCJpbmJveF9pZCI6MTA5MzIxLCJleHAiOjE3OTQ0MDM4NTEsImlhdCI6MTc3ODg1MTg1MX0.vpHZTgUopVaF_3bFv4vcEw2Ef1Bd1OUBhro18c1ZuHs; kt_vid=056391202fa84982a161f35402b19925; server_session_afa45114=6a50d204b5630e5e2f90a57904af65b6; selectedSourceKey=Line1; PHPSESSID=9tk1latt66i6lsjbhfse18otbq; kt_ips=120.234.36.82%2C183.239.165.202; kt_sid=e8a74ca61fa5e9d6.1789549756"
  }
});

// 简单 Cookie Jar
let cookies = {};

function saveCookies(response) {
  const setCookie = response.headers["set-cookie"];

  if (!setCookie) {
    return;
  }

  for (const cookie of setCookie) {
    const pair = cookie.split(";")[0];
    const index = pair.indexOf("=");

    if (index === -1) continue;

    const name = pair.substring(0, index);
    const value = pair.substring(index + 1);

    cookies[name] = value;
  }
}

function getCookieHeader() {
  return Object.entries(cookies)
    .map(([key, value]) => `${key}=${value}`)
    .join("; ");
}

async function login() {
  console.log("正在登录...");

  const response = await client.post(
    "/login",
    {
      username: USERNAME,
      password: PASSWORD
    },
    {
      headers: {
        Cookie: getCookieHeader()
      }
    }
  );

  saveCookies(response);

  console.log(`登录 HTTP 状态码: ${response.status}`);

  if (response.status < 200 || response.status >= 300) {
    throw new Error(`登录失败: ${JSON.stringify(response.data)}`);
  }

  console.log("登录成功");
}

async function checkIn() {
  console.log("正在签到...");

  const response = await client.post(
    "/mod/sing_in.php",
    {},
    {
      headers: {
        Cookie: getCookieHeader()
      }
    }
  );

  saveCookies(response);

  console.log(`签到 HTTP 状态码: ${response.status}`);

  if (response.status < 200 || response.status >= 300) {
    throw new Error(`签到失败: ${JSON.stringify(response.data)}`);
  }

  console.log("签到请求完成");
  console.log("服务器返回:");
  console.log(response.data);
}

async function main() {
  try {
    await login();
    await checkIn();

    console.log("任务执行完成");
  } catch (error) {
    console.error("任务执行失败:");

    if (error.response) {
      console.error("HTTP:", error.response.status);
      console.error("Response:", error.response.data);
    } else {
      console.error(error.message);
    }

    process.exit(1);
  }
}

main();
