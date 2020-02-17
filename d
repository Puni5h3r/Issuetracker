[1mdiff --git a/.idea/workspace.xml b/.idea/workspace.xml[m
[1mindex ad34bec..631b258 100644[m
[1m--- a/.idea/workspace.xml[m
[1m+++ b/.idea/workspace.xml[m
[36m@@ -1,7 +1,13 @@[m
 <?xml version="1.0" encoding="UTF-8"?>[m
 <project version="4">[m
   <component name="ChangeListManager">[m
[31m-    <list default="true" id="5160d085-c42f-4b32-aee6-d0d5d4245797" name="Default Changelist" comment="" />[m
[32m+[m[32m    <list default="true" id="5160d085-c42f-4b32-aee6-d0d5d4245797" name="Default Changelist" comment="">[m
[32m+[m[32m      <change afterPath="$PROJECT_DIR$/.idea/vcs.xml" afterDir="false" />[m
[32m+[m[32m      <change beforePath="$PROJECT_DIR$/.idea/workspace.xml" beforeDir="false" afterPath="$PROJECT_DIR$/.idea/workspace.xml" afterDir="false" />[m
[32m+[m[32m      <change beforePath="$PROJECT_DIR$/base/views.py" beforeDir="false" afterPath="$PROJECT_DIR$/base/views.py" afterDir="false" />[m
[32m+[m[32m      <change beforePath="$PROJECT_DIR$/db.sqlite3" beforeDir="false" afterPath="$PROJECT_DIR$/db.sqlite3" afterDir="false" />[m
[32m+[m[32m      <change beforePath="$PROJECT_DIR$/update/views.py" beforeDir="false" afterPath="$PROJECT_DIR$/update/views.py" afterDir="false" />[m
[32m+[m[32m    </list>[m
     <option name="SHOW_DIALOG" value="false" />[m
     <option name="HIGHLIGHT_CONFLICTS" value="true" />[m
     <option name="HIGHLIGHT_NON_ACTIVE_CHANGELIST" value="false" />[m
[36m@@ -15,7 +21,11 @@[m
       </list>[m
     </option>[m
   </component>[m
[32m+[m[32m  <component name="Git.Settings">[m
[32m+[m[32m    <option name="RECENT_GIT_ROOT_PATH" value="$PROJECT_DIR$" />[m
[32m+[m[32m  </component>[m
   <component name="ProjectId" id="1XiF61smG1pPBqOVYiT6gD9bDqh" />[m
[32m+[m[32m  <component name="ProjectLevelVcsManager" settingsEditedManually="true" />[m
   <component name="ProjectViewState">[m
     <option name="hideEmptyMiddlePackages" value="true" />[m
     <option name="showExcludedFiles" value="true" />[m
[36m@@ -24,6 +34,7 @@[m
   <component name="PropertiesComponent">[m
     <property name="DefaultHtmlFileTemplate" value="HTML File" />[m
     <property name="RunOnceActivity.ShowReadmeOnStart" value="true" />[m
[32m+[m[32m    <property name="SHARE_PROJECT_CONFIGURATION_FILES" value="true" />[m
     <property name="last_opened_file_path" value="$USER_HOME$/Work/Apploye/groupboss/groupboss" />[m
     <property name="settings.editor.selected.configurable" value="com.jetbrains.python.configuration.PyActiveSdkModuleConfigurable" />[m
   </component>[m
[36m@@ -50,10 +61,10 @@[m
     <servers />[m
   </component>[m
   <component name="WindowStateProjectService">[m
[31m-    <state x="633" y="342" width="710" height="421" key="#com.intellij.fileTypes.FileTypeChooser" timestamp="1581841912264">[m
[32m+[m[32m    <state x="633" y="342" width="710" height="421" key="#com.intellij.fileTypes.FileTypeChooser" timestamp="1581908929110">[m
       <screen x="67" y="27" width="1853" height="1053" />[m
     </state>[m
[31m-    <state x="633" y="342" width="710" height="421" key="#com.intellij.fileTypes.FileTypeChooser/67.27.1853.1053@67.27.1853.1053" timestamp="1581841912264" />[m
[32m+[m[32m    <state x="633" y="342" width="710" height="421" key="#com.intellij.fileTypes.FileTypeChooser/67.27.1853.1053@67.27.1853.1053" timestamp="1581908929110" />[m
     <state x="717" y="255" width="524" height="594" key="FileChooserDialogImpl" timestamp="1581891578864">[m
       <screen x="67" y="27" width="1853" height="1053" />[m
     </state>[m
[1mdiff --git a/base/__pycache__/views.cpython-36.pyc b/base/__pycache__/views.cpython-36.pyc[m
[1mindex f71f2a5..85cc80e 100644[m
Binary files a/base/__pycache__/views.cpython-36.pyc and b/base/__pycache__/views.cpython-36.pyc differ
[1mdiff --git a/base/views.py b/base/views.py[m
[1mindex 6586338..ee0caf9 100644[m
[1m--- a/base/views.py[m
[1m+++ b/base/views.py[m
[36m@@ -141,5 +141,4 @@[m [mdef create_issue(request, id):[m
             issue.save()[m
             return redirect('base:project_detail', id = id)[m
 [m
[31m-[m
     return render(request,'projects/create_issue_template.html',context)[m
\ No newline at end of file[m
[1mdiff --git a/db.sqlite3 b/db.sqlite3[m
[1mindex 2845a20..0aecc58 100644[m
Binary files a/db.sqlite3 and b/db.sqlite3 differ
[1mdiff --git a/update/__pycache__/views.cpython-36.pyc b/update/__pycache__/views.cpython-36.pyc[m
[1mindex 7f060ae..a362ace 100644[m
Binary files a/update/__pycache__/views.cpython-36.pyc and b/update/__pycache__/views.cpython-36.pyc differ
[1mdiff --git a/update/views.py b/update/views.py[m
[1mindex fd82130..eb12b58 100644[m
[1m--- a/update/views.py[m
[1m+++ b/update/views.py[m
[36m@@ -11,8 +11,12 @@[m [mdef update_issue(request,id):[m
     comment = IssueComment.objects.filter(issue=issue)[m
     form2 = IssueCommentForm[m
     project = Project.objects.get(pk = issue.project.project_id)[m
[31m-    like = IssueLike.objects.get(issue = issue or None)[m
[31m-    form3 = IssueLikeForm(instance=like)[m
[32m+[m[32m    try:[m
[32m+[m[32m        like_instance = IssueLike.objects.get(issue = issue)[m
[32m+[m[32m        form3 = IssueLikeForm(instance=like_instance)[m
[32m+[m[32m    except IssueLike.DoesNotExist:[m
[32m+[m[32m        form3 = IssueLikeForm[m
[32m+[m[32m        like_instance = None[m
 [m
     if request.method == "POST":[m
         form = IssueCloseForm(request.POST, instance=issue)[m
[36m@@ -26,26 +30,34 @@[m [mdef update_issue(request,id):[m
             post = form.save(commit=False)[m
             post.updated_by_user = request.user[m
             post.save()[m
[31m-            like = request.POST.get('like' or None)[m
[31m-            dislike = request.POST.get('dislike' or None)[m
[31m-            if like or dislike is True:[m
[32m+[m[32m            if like_instance is None:[m
                 issue_like = form3.save(commit=False)[m
                 issue_like.issue = issue[m
                 issue_like.action_by = request.user[m
                 issue_like.save()[m
[32m+[m[32m            else:[m
[32m+[m[32m                issue_like = form3.save(commit=False)[m
[32m+[m[32m                obj, created = IssueLike.objects.update_or_create([m
[32m+[m[32m                    issue=issue, action_by=request.user,[m
[32m+[m[32m                    defaults={'like': issue_like.like, 'dislike':issue_like.dislike},[m
[32m+[m[32m                )[m
             return redirect('update:update_issue', id=issue.id)[m
         elif form.is_valid() :[m
             post = form.save(commit=False)[m
             post.updated_by_user = request.user[m
             post.save()[m
[31m-            like = request.POST.get('like' or None)[m
[31m-            dislike = request.POST.get('dislike' or None)[m
[31m-            if like or dislike is True:[m
[32m+[m[32m            if like_instance is None:[m
                 issue_like = form3.save(commit=False)[m
                 issue_like.issue = issue[m
                 issue_like.action_by = request.user[m
                 issue_like.save()[m
[31m-            return redirect('base:project_detail', id = project.project_id )[m
[32m+[m[32m            else:[m
[32m+[m[32m                issue_like = form3.save(commit=False)[m
[32m+[m[32m                obj, created = IssueLike.objects.update_or_create([m
[32m+[m[32m                    issue=issue, action_by=request.user,[m
[32m+[m[32m                    defaults={'like': issue_like.like, 'dislike': issue_like.dislike},[m
[32m+[m[32m                )[m
[32m+[m[32m            return redirect('update:update_issue', id = issue.id )[m
 [m
     context = {'form': form,[m
                'form2':form2,[m
