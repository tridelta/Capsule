from . import ConfigService
from . import index
from . import AIService
from . import AutoOrganizeService
from . import FileService
from . import inverse_index
from . import schema
from . import utils
from . import test


if __name__ == "__main__":
    test.app.run(host="::0", port=5201, debug=True)
