const en = {
  common: {
    logout: 'Logout',
  },
  auth: {
    signIn: 'Sign in',
    signUp: 'Sign up',
    email: 'Email',
    password: 'Password',
    confirmPassword: 'Confirm password',
    signInSubtitle: 'manyS — VK content planner',
    signupSubtitle: 'Start planning content for your VK groups',
    fillAllFields: 'Fill in all fields',
    atLeast8: 'At least 8 characters',
    passwordMin8: 'Password must be at least 8 characters',
    passwordsMismatch: 'Passwords do not match',
    noAccount: 'No account?',
    haveAccount: 'Already have an account?',
  },
  board: {
    wallPosts: 'Wall posts',
    postponed: 'Postponed',
  },
  group: {
    group: 'Group',
    domain: 'VK group domain',
    load: 'Load',
  },
  feed: {
    noPosts: 'No posts found for this group.',
    all: "That's all",
    scrollMore: 'Scroll for more',
  },
  post: {
    pinned: 'Pinned',
    fallback: 'Post',
  },
  postponed: {
    title: 'Postponed posts',
    text: 'Text',
    attachMedia: 'Attach media',
    removeFile: 'Remove file',
    schedule: 'Schedule',
    nothingYet: 'Nothing postponed yet.',
    mediaOnly: '(media only)',
    enterTextOrFile: 'Enter text or attach a file',
    created: 'Postponed post created',
  },
  errors: {
    requestFailed: 'Request failed ({{status}})',
    unexpected: 'Unexpected error',
  },
};

export type Translation = typeof en;
export default en;
