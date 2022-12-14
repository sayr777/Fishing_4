from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy import platform
from dialog import Dialog

class News(Screen):
    def click_on_button_go_chat(self):
        if platform == 'android': #check if the app is on Android
            import jnius
            from jnius import cast
            from jnius import autoclass
            appName = "org.telegram.messenger"
            PythonActivity = autoclass('org.kivy.android.PythonActivity') #request the Kivy activity instance
            Intent = autoclass('android.content.Intent') # get the Android Intend clast
            String = autoclass('java.lang.String')
            currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
            Context = autoclass('android.content.Context')
            pm = currentActivity.getApplicationContext().getPackageManager();
            Uri = autoclass('android.net.Uri')
            flag = False
            try:
                pm.getPackageInfo(cast('java.lang.CharSequence', String('org.telegram.messenger')), PackageManager.GET_ACTIVITIES);
                flag = True;
            except:
                flag = True;

            if flag:
                uri = Uri.parse('https://telegram.me/+ZNRNXnSbanxmZTQy')
                intent = Intent(Intent.ACTION_VIEW)
                intent.setData(uri)
                currentActivity.startActivity(intent) # show the intent in the game activity
            else:
                Dialog('Telegram не установлен', 'Внимание')
