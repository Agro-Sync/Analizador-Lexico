from playwright.sync_api import sync_playwright
import time, os, logging

logging.basicConfig(level=logging.INFO)

class AWS:
    def __init__(self, email, password, headless=True):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

        logging.info("[+] Navegador iniciado")
        self._login(email, password)

    def _login(self, email, password):
        """Realiza login no portal AWS Academy."""
        logging.info("[*] Fazendo login...")
        self.page.goto("https://www.awsacademy.com/vforcesite/LMS_Login")

        self.page.click('body > div.splash-body > a:nth-child(1) > button')

        self.page.fill("#pseudonym_session_unique_id", email)
        self.page.fill("#pseudonym_session_password", password)

        self.page.click('#login_form > div.ic-Login__actions > div.ic-Form-control.ic-Form-control--login > input')

        logging.info("[+] Login concluído com sucesso")


    def configure_aws(self, conta):
        """Configura a conta da AWS para consulta"""
        logging.info("[+] Entrando na AWS")
        self.page.goto(f"https://awsacademy.instructure.com/courses/{conta}/modules/items/12498015")
        self.page.wait_for_load_state("domcontentloaded", timeout=0)

        logging.info('[*] Verificando status da conta')
        frame_locator = self.page.frame_locator('iframe.tool_launch')
        try:
            locator = frame_locator.locator('#vmstatus')
            locator.wait_for(state='attached', timeout=30000)
            classe = locator.get_attribute('class')
        except Exception as e:
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            timestamp = int(time.time())
            path = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")
            self.page.screenshot(path=path)
            logging.info(f"Screenshot salvo em: {path}")

        if 'led-green' not in classe:
            logging.info('[*] Inicia a conta da AWS')
            frame_locator.locator('#launchclabsbtn').click()
            frame_locator.locator('#vmstatus.led-green').wait_for(timeout=0)

        logging.info("[*] Coletando informações da AWS")
        # mostrar informações aws
        frame_locator.locator('#detailbtn2').click()
        frame_locator.locator('#clikeyboxbtn').click()

        # coletar texto
        text_locator = frame_locator.locator('#clikeybox > pre > span')
        text_locator.wait_for(state='attached', timeout=0)
        return text_locator.text_content()


    @staticmethod
    def get_secrets(info_raw):
        info = info_raw.split()

        aws_access_key_id = info[1].split('=')[1]
        aws_secret_access_key = info[2].split('=')[1]
        aws_session_token = info[3].split('=', 1)[1]
        logging.info('[+] Dados coletados')
        return aws_access_key_id, aws_secret_access_key, aws_session_token

def set_github_env(aws_access_key_id, aws_secret_access_key, aws_session_token):
    with open(os.environ['GITHUB_ENV'], 'a') as env_file:
        env_file.write(f"AWS_ACCESS_KEY_ID={aws_access_key_id}\n")
        env_file.write(f"AWS_SECRET_ACCESS_KEY={aws_secret_access_key}\n")
        env_file.write(f"AWS_SESSION_TOKEN={aws_session_token}\n")

if __name__ == "__main__":
    import os

    email = os.environ["EMAIL"]
    senha = os.environ["PASSWORD"]
    conta = "130670"

    aws = AWS(email, senha)
    info_raw = aws.configure_aws(conta)
    aws_access_key_id, aws_secret_access_key, aws_session_token = aws.get_secrets(info_raw)
    set_github_env(aws_access_key_id, aws_secret_access_key, aws_session_token)