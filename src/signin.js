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
  
  const params = new URLSearchParams();
  params.append('username', '张三');
  params.append('pass', '123456');
  
  const response = await client.post(
    "/login",
    params,
    {
      headers: {
        Cookie: getCookieHeader(),
        "content-type":"application/x-www-form-urlencoded; charset=UTF-8"
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
    {"action":"sign_in","lang":"zh","user_id":185920,"csrf_token":""},
    {
      headers: {
        Cookie: getCookieHeader(),
       "content-type":"application/json; charset=UTF-8"

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
